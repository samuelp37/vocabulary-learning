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
    
    def create_autocomplete_form(self,model=models.Author,modelForm=forms.AuthorForm,prefix="author",title="Author",label_field="first_name"):
    
        form = modelForm(prefix=prefix)
        target_input_id = "#id_"+form.prefix+"-"+label_field
        form.title = title
        form.list_fields = get_all_fields_from_form(modelForm)
    
        queryset = model.objects.all()
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
        formA, target_input_id, authors = self.create_autocomplete_form(model=models.Author,modelForm=forms.AuthorForm,prefix="author",title="Author",label_field="first_name")
            
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
        
class CreateTranslationView(LoginRequiredMixin,AutoCompletionNestedView):

    def get(self, request,slug=None):
        
        target_input_words = []
        
        #creating a new form
        form = forms.TranslationForm()
        formA, target_input_id, words = self.create_autocomplete_form(model=models.Word,modelForm=forms.WordForm,prefix="original",title="Original word",label_field="word")
        target_input_words.append(target_input_id)
        formB, target_input_id, words = self.create_autocomplete_form(model=models.Word,modelForm=forms.WordForm,prefix="translate",title="Translated word",label_field="word") 
        target_input_words.append(target_input_id)
        target_input_words = ",".join(target_input_words)
           
        print(words) 
          
        return render(request, 'dictionary/vocform.html', {'form':form,'formA':formA,'formB':formB,'words':words,'target_input_words':target_input_words})

    def post(self, request,slug=None):
        
        formA = forms.WordForm(request.POST,prefix="original")
        formB = forms.WordForm(request.POST,prefix="translate")
        form = forms.TranslationForm(request.POST)
        
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

"""
class LecturesListView(ListView):

	model = Lecture
	paginate_by = 10  # if pagination is desired
	template_name = "dictionary/lectures_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
"""