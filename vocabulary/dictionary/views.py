from django.shortcuts import render, get_object_or_404
from . import forms
from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView
from django.views.generic.base import View
from . import models
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
import random
import string
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from extra_views import CreateWithInlinesView, InlineFormSet
from django.db import models as djangoModel

def get_all_fields_from_form(instance):
    """"
    Return names of all available fields from given Form instance.

    :arg instance: Form instance
    :returns list of field names
    :rtype: list
    """

    fields = list(instance().base_fields)

    for field in list(instance().declared_fields):
        if field not in fields:
            fields.append(field)
    return fields

class HomeNoMemberView(TemplateView):

    template_name = 'dictionary/home_nomember.html'

class HomeMemberView(LoginRequiredMixin,TemplateView):

    template_name = 'dictionary/home_member.html'
        
def random_str(n):
    return ''.join(random.choice(string.ascii_letters) for x in range(n))

class AutoCompletionNestedView(View):
    
    def create_autocomplete_form(self,request,model=models.Author,modelForm=forms.AuthorForm,prefix="author",title="Author",label_field="first_name",user_based=False,pre_instance=None):
        
        if pre_instance is None:
            form = modelForm(prefix=prefix)
        else:
            form = modelForm(None, prefix=prefix, instance=pre_instance)
        
        target_input_id = "#id_"+form.prefix+"-"+label_field
        form.title = title
        form.list_fields = get_all_fields_from_form(modelForm)
    
        if not user_based:
            queryset = model.objects.all()
        else:
            queryset = model.objects.all().filter(user=request.user)
        dict_instances = {}
        for i in range(len(queryset)):
            tmp = queryset[i]
            dict_instances[i] = []
            for field_name in form.list_fields:
                attr = getattr(tmp, field_name)
                if isinstance(attr,djangoModel.Model):
                    dict_instances[i].append(attr.id)
                else:
                    dict_instances[i].append(attr)
            dict_instances[i].append(tmp.__str__())
                
        return form, target_input_id, dict_instances
    
class CreateBookView(LoginRequiredMixin,AutoCompletionNestedView):

    def get(self, request):
        
        target_input_words = []
        
        #creating a new form
        form = forms.BookForm()
        formA, target_input_id, authors = self.create_autocomplete_form(request,model=models.Author,modelForm=forms.AuthorForm,prefix="author",title="Author",label_field="first_name",user_based=False)
            
        target_input_words.append(target_input_id)
        target_input_words = ",".join(target_input_words)
           
        return render(request, 'dictionary/bookform.html', {'form':form,'formA':formA,'authors':authors,'target_input_words':target_input_words})

    def post(self, request):
        
        form = forms.BookForm(request.POST)
        formA = forms.AuthorForm(request.POST,prefix="author")
        
        # Adding the 2 words
        if formA.is_valid():
            authorA, boolA = models.Author.objects.get_or_create(**formA.cleaned_data)
            
            if form.is_valid():
                book = form.save(commit=False)
                book.author = authorA
                book.user = request.user
                book.slug = slugify(book.title)
                book.save()
                return HttpResponseRedirect(reverse('list_book'))
        
        return self.get(request)
 
class TranslationForeignKeyTranslationField(AutoCompletionNestedView):

    def __init__(self,model,modelForm,label_field,user_based=False):
    
        self.model = model
        self.modelForm = modelForm
        self.label_field = label_field
        self.user_based = user_based
        self.original_prefix = "original_"+self.label_field
        self.translate_prefix = "translated_"+self.label_field
        
    def initialize_get(self,request,pre_instance=None):
    
        self.target_input_words = []
        if pre_instance is None:
            self.formA, self.target_input_id, self.suggestion = self.create_autocomplete_form(request,model=self.model,modelForm=self.modelForm,prefix=self.original_prefix,title="Original "+self.label_field,label_field=self.label_field,user_based=self.user_based)
        else:
            self.formA, self.target_input_id, self.suggestion = self.create_autocomplete_form(request,model=self.model,modelForm=self.modelForm,prefix=self.original_prefix,title="Original "+self.label_field,label_field=self.label_field,user_based=self.user_based, pre_instance=getattr(pre_instance,self.original_prefix))            
        self.target_input_words.append(self.target_input_id)
        if pre_instance is None:
            self.formB, self.target_input_id, _ = self.create_autocomplete_form(request,model=self.model,modelForm=self.modelForm,prefix=self.translate_prefix,title="Translated "+self.label_field,label_field=self.label_field,user_based=self.user_based) 
        else:
            self.formB, self.target_input_id, _ = self.create_autocomplete_form(request,model=self.model,modelForm=self.modelForm,prefix=self.translate_prefix,title="Translated "+self.label_field,label_field=self.label_field,user_based=self.user_based, pre_instance=getattr(pre_instance,self.translate_prefix))             
        self.target_input_words.append(self.target_input_id)
        self.target_input_words = ",".join(self.target_input_words)
        
    def initialize_post(self,request):
    
        print(request.POST)
    
        self.formA = self.modelForm(request.POST,prefix=self.original_prefix)
        self.formB = self.modelForm(request.POST,prefix=self.translate_prefix)
        self.itemA, self.itemB = None, None
        print(self.formA)
        
        if self.formA.is_valid() and self.formB.is_valid():
            self.itemA, boolA = self.model.objects.get_or_create(**self.formA.cleaned_data)
            self.itemB, boolB = self.model.objects.get_or_create(**self.formB.cleaned_data)
            return True
        else:
            print(self.formA.errors)
            print(self.formB.errors)
            
        return False
            
    def update_main_form(self,form):
   
        setattr(form, self.original_prefix, self.itemA)
        setattr(form, self.translate_prefix, self.itemB)
        setattr(form, "slug", slugify(self.itemA.__str__() + "-" + self.itemB.__str__()))
        
    def update_variables_dict(self,variables_dict):
        new_dict = {}
        new_dict['formA_'+self.label_field] = self.formA
        new_dict['formB_'+self.label_field] = self.formB
        new_dict['suggestion_'+self.label_field] = self.suggestion
        variables_dict['target_input_words'] += self.target_input_words
        variables_dict.update(new_dict)

class CreateTranslationView(LoginRequiredMixin,AutoCompletionNestedView):

    def initalize_nested_fields(self):
        self.nested_fields = []
        self.nested_fields.append(TranslationForeignKeyTranslationField(model=models.Word,modelForm=forms.WordForm,label_field="word"))

    def get(self, request,slug=None):
        
        if "slug" in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = None
        
        # Getting nested_fields
        self.initalize_nested_fields()
        
        # Creating a new form
        form = forms.TranslationForm()
        variables_dict = {'form':form,'slug':slug,'target_input_words':""}
        
        # Creating nested forms
        for field in self.nested_fields:
            field.initialize_get(request)
            field.update_variables_dict(variables_dict)
          
        return render(request, 'dictionary/vocform.html', variables_dict)

    def post(self, request, slug=None):
    
        # Initialize main form
        form = forms.TranslationForm(request.POST)
    
        # Getting nested_fields
        self.initalize_nested_fields()
        
        success = True
        for field in self.nested_fields:
            success = field.initialize_post(request)
            if not success:
                break
        
        print("Success : "+str(success))
        
        if success:
            
            if form.is_valid():
                translate = form.save(commit=False)
                for field in self.nested_fields:
                    field.update_main_form(translate)
                translate.user = request.user
                translate_item = translate.save()
                
                if slug!=None:
                    book = get_object_or_404(models.Book, slug=slug)
                    translation_link = models.TranslationLink()
                    translation_link.item = translate
                    translation_link.book = book
                    id_translationlink = translation_link.save()
                    return HttpResponseRedirect(reverse('details_book', kwargs={'slug':slug}))
                    
                return HttpResponseRedirect(reverse('list_translations'))
    
        return self.get(request)
   
class BooksListView(LoginRequiredMixin,ListView):

    model = models.Book
    paginate_by = 10  # if pagination is desired
    template_name = "dictionary/books_list.html"
    
    def get_queryset(self):
        return models.Book.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TranslationListView(LoginRequiredMixin,ListView):

    model = models.Translation
    paginate_by = 10  # if pagination is desired
    template_name = "dictionary/translation_list.html"
     
    def get_queryset(self):
        return models.Translation.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AuthorizeAccessDetailView(View):

    def get(self, request, slug):
        obj = super().get_object()
        if obj.user != request.user:
            return HttpResponseForbidden('Unauthorized access')
        
        return super().get(self, request, slug)
    
class BookView(LoginRequiredMixin,DetailView,AuthorizeAccessDetailView):

    model = models.Book
    template_name = 'dictionary/book_detail.html'
    slug_url_kwarg = 'slug'
        
class UpdateBookView(LoginRequiredMixin,UpdateView,AuthorizeAccessDetailView):

    model = models.Book
    fields=["title","language","author","subtitle","nb_pages"]
    template_name = 'dictionary/book_update.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'book'
        
    def get_success_url(self):
        return reverse('details_book', kwargs={'slug':self.kwargs['slug']})
        
class TranslationView(LoginRequiredMixin,DetailView,AuthorizeAccessDetailView):

    model = models.Translation
    template_name = 'dictionary/translation_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'translation'

class UpdateTranslationView(LoginRequiredMixin,AutoCompletionNestedView):

    def initalize_nested_fields(self):
        self.nested_fields = []
        self.nested_fields.append(TranslationForeignKeyTranslationField(model=models.Word,modelForm=forms.WordForm,label_field="word"))

    def get(self, request,slug):
        
        if "slug" in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = None
        
        # Getting nested_fields
        self.initalize_nested_fields()
        
        # Getting pre-instance
        pre_instance = get_object_or_404(models.Translation, slug=self.kwargs['slug'])
        
        # Creating a new form
        form = forms.TranslationForm(None, instance=pre_instance)
        variables_dict = {'form':form,'slug':slug,'target_input_words':""}
        
        # Creating nested forms
        for field in self.nested_fields:
            field.initialize_get(request,pre_instance)
            field.update_variables_dict(variables_dict)
          
        return render(request, 'dictionary/translation_update.html', variables_dict)

    def post(self, request, slug):
    
        pre_instance = get_object_or_404(models.Translation, slug=self.kwargs['slug'])
        form = forms.TranslationForm(request.POST,instance=pre_instance)
    
        # Getting nested_fields
        self.initalize_nested_fields()
        
        success = True
        for field in self.nested_fields:
            success = field.initialize_post(request)
            if not success:
                break
        
        print("Success : "+str(success))
        
        if success:
            
            if form.is_valid():
                translate = form.save(commit=False)
                for field in self.nested_fields:
                    field.update_main_form(translate)
                translate.user = request.user
                translate_item = translate.save()
                    
                return HttpResponseRedirect(reverse('list_translations'))
    
        return self.get(request)
"""
class UpdateTranslationView(LoginRequiredMixin,UpdateView,AuthorizeAccessDetailView,AutoCompletionNestedView):

    model = models.Translation
    fields=["original_word","translated_word","context_sentence","translation_context_sentence"]
    template_name = 'dictionary/translation_update.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'translation'
    
    def get(self, request,slug=None):
        
        target_input_words = []
        
        # Getting pre-instance
        pre_instance = get_object_or_404(models.Translation, slug=self.kwargs['slug'])
        
        #creating a new form
        form = forms.TranslationForm(None, instance=pre_instance)
        formA, target_input_id, words = self.create_autocomplete_form(request,model=models.Word,modelForm=forms.WordForm,prefix="original",title="Original word",label_field="word",pre_instance=pre_instance.original_word)
        target_input_words.append(target_input_id)
        formB, target_input_id, words = self.create_autocomplete_form(request,model=models.Word,modelForm=forms.WordForm,prefix="translate",title="Translated word",label_field="word",pre_instance=pre_instance.translated_word) 
        target_input_words.append(target_input_id)
        target_input_words = ",".join(target_input_words)
          
        return render(request, 'dictionary/translation_update.html', {'slug':self.kwargs['slug'],'form':form,'formA':formA,'formB':formB,'words':words,'target_input_words':target_input_words})
    
    def post(self, request,slug=None):
        
        formA = forms.WordForm(request.POST,prefix="original")
        formB = forms.WordForm(request.POST,prefix="translate")
        pre_instance = get_object_or_404(models.Translation, slug=self.kwargs['slug'])
        form = forms.TranslationForm(request.POST,instance=pre_instance)
        
        # Adding the 2 words
        if formA.is_valid() and formB.is_valid():
            wordA, boolA = models.Word.objects.get_or_create(**formA.cleaned_data)
            wordB, boolB = models.Word.objects.get_or_create(**formB.cleaned_data)
            form.original_word = wordA
            form.translated_word = wordB
            
            if form.is_valid():
                translate = form.save(commit=False)
                translate.original_word = wordA
                translate.translated_word = wordB
                translate.slug = slugify(wordA.word+"-"+wordB.word)
                translate_item = translate.save()
                return HttpResponseRedirect(reverse('details_translation', kwargs={'slug':translate.slug}))
        
        return self.get(request)
    
"""
"""
class LecturesListView(ListView):

	model = Lecture
	paginate_by = 10  # if pagination is desired
	template_name = "dictionary/lectures_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
"""