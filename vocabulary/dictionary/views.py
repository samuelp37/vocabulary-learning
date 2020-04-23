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
import sys

from .views_common import *

class HomeNoMemberView(TemplateView):

    template_name = 'dictionary/home_nomember.html'

class HomeMemberView(LoginRequiredMixin,TemplateView):

    template_name = 'dictionary/home_member.html'
    
class WordAutocompleteView(LoginRequiredMixin,View,AutoCompletionNestedField):

    def __init__(self):
        AutoCompletionNestedField.__init__(self,model_name="Word",model_form_name="WordForm",field_autocomplete_name="word",prefix=None,title=None,user_based=False)

class AuthorAutocompleteView(LoginRequiredMixin,View,AutoCompletionNestedField):

    def __init__(self):
        AutoCompletionNestedField.__init__(self,model_name="Author",model_form_name="AuthorForm",field_autocomplete_name="first_name",prefix=None,title=None,user_based=False)

  
class CreateBookView(LoginRequiredMixin,View):

    def initalize_nested_fields(self):
        self.nested_field = AutoCompletionNestedField(model_name="Author",model_form_name="AuthorForm",field_autocomplete_name="first_name",prefix="author",title="Author",user_based=False)

    def get(self, request):
        
        target_input_words = []
        
        # Getting nested_fields
        self.initalize_nested_fields()
        
        #creating a new form
        form = forms.BookForm()
        formA, target_input_id = self.nested_field.autocomplete_form(request)
            
        target_input_words.append(target_input_id)
        target_input_words = ",".join(target_input_words)
        print(target_input_words)
           
        return render(request, 'dictionary/bookform.html', {'form':form,'formA':formA,'target_input_words':target_input_words})

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

class CreateTranslationView(LoginRequiredMixin,View):

    def initalize_nested_fields(self):
        self.nested_fields = []
        self.nested_fields.append(TranslationForeignKeyTranslationField(model_name="Word",model_form_name="WordForm",field_autocomplete_name="word",user_based=False))

    def get(self, request, slug_book=None):
    
        # Getting nested_fields
        self.initalize_nested_fields()
        
        # Creating a new form
        form = forms.TranslationForm()
        variables_dict = {'form':form,'slug_book':slug_book,'target_input_words':""}
        
        # Creating nested forms
        for field in self.nested_fields:
            field.initialize_get(request)
            field.update_variables_dict(variables_dict)
          
        return render(request, 'dictionary/vocform.html', variables_dict)

    def post(self, request, slug_book=None):
    
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
                
                if slug_book!=None:
                    book = get_object_or_404(models.Book, slug=slug_book)
                    translation_link = models.TranslationLink()
                    translation_link.item = translate
                    translation_link.book = book
                    id_translationlink = translation_link.save()
                    return HttpResponseRedirect(reverse('details_book', kwargs={'slug':slug_book}))
                    
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
    slug_url_kwarg = 'slug_book'
    
    def get_object(self):
        return get_object_or_404(models.Book,slug=self.kwargs['slug_book'])
        
class UpdateBookView(LoginRequiredMixin,UpdateView,AuthorizeAccessDetailView):

    model = models.Book
    fields=["title","language","author","subtitle","nb_pages"]
    template_name = 'dictionary/book_update.html'
    slug_url_kwarg = 'slug_book'
    context_object_name = 'book'
        
    def get_success_url(self):
        return reverse('details_book', kwargs={'slug_book':self.kwargs['slug_book']})
        
class TranslationView(LoginRequiredMixin,DetailView,AuthorizeAccessDetailView):

    model = models.Translation
    template_name = 'dictionary/translation_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'translation'
    
    def get_object(self):
        return get_object_or_404(models.Translation,slug=self.kwargs['slug'])
        
    def get_context_data(self, **kwargs):
        context = super(TranslationView, self).get_context_data(**kwargs)
        if 'slug_book' in self.kwargs:
            context['slug_book'] = self.kwargs['slug_book']
        return context

class UpdateTranslationView(LoginRequiredMixin,View):

    def initalize_nested_fields(self):
        self.nested_fields = []
        self.nested_fields.append(TranslationForeignKeyTranslationField(model_name="Word",model_form_name="WordForm",field_autocomplete_name="word",user_based=False))

    def get(self, request,slug,slug_book=None):
        
        # Getting nested_fields
        self.initalize_nested_fields()
        
        # Getting pre-instance
        pre_instance = get_object_or_404(models.Translation, slug=self.kwargs['slug'])
        print(pre_instance)
        
        # Creating a new form
        form = forms.TranslationForm(instance=pre_instance)
        variables_dict = {'form':form,'slug':self.kwargs['slug'],'slug_book':slug_book,'target_input_words':""}
        
        # Creating nested forms
        for field in self.nested_fields:
            field.initialize_get(request,pre_instance)
            field.update_variables_dict(variables_dict)
          
        return render(request, 'dictionary/translation_update.html', variables_dict)

    def post(self, request, slug, slug_book=None):
        
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
                if slug_book is None:  
                    return HttpResponseRedirect(reverse('list_translations'))
                else:
                    return HttpResponseRedirect(reverse('details_book', kwargs={'slug_book':slug_book}))
        else:
            print(form.errors)
        
        return self.get(request,slug)