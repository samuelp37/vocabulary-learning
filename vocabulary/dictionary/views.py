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
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from extra_views import CreateWithInlinesView, InlineFormSet
import sys
from django.db.models import Q

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

class CreateUpdateBookView(LoginRequiredMixin,View):

    def initalize_nested_fields(self):
        self.nested_fields = []
        self.nested_fields.append(AutoCompletionNestedField(model_name="Author",model_form_name="AuthorForm",field_autocomplete_name="first_name",prefix="author",title="Author",user_based=False))

    def get(self, request, slug_book=None):
        
        target_input_words = []
        
        # Getting nested_fields
        self.initalize_nested_fields()
        
        # Getting pre-instance
        pre_instance = models.Book.objects.filter(slug=slug_book).first()
        
        # Creating a new form
        if pre_instance is None:
            form = forms.BookForm()
        else:
            form = forms.BookForm(instance=pre_instance)
            
        variables_dict = {'form':form,'slug_book':slug_book,'target_input_words':""}
          
        #creating nested form Author
        formA, target_input_id = self.nested_fields[0].autocomplete_form(request,pre_instance)
            
        target_input_words.append(target_input_id)
        target_input_words = ",".join(target_input_words)
        
        return render(request, 'dictionary/bookform.html', {'form':form,'formA':formA,'slug_book':slug_book,'target_input_words':target_input_words})

    def post(self, request,slug_book=None):
    
        # Initialize main form
        pre_instance = models.Book.objects.filter(slug=slug_book).first()
        
        if pre_instance is None:
            form = forms.BookForm(request.POST)
            update = False
        else:
            form = forms.BookForm(request.POST,instance=pre_instance)
            update = True
    
        # Getting nested_fields
        self.initalize_nested_fields()
        
        success = True
        for field in self.nested_fields:
            success = field.initialize_post(request)
            if not success:
                break
        
        if success:
            
            if form.is_valid():
                book = form.save(commit=False)
                for field in self.nested_fields:
                    field.update_main_form(book)
                book.user = request.user
                book.slug = slugify(book.title)
                book.save()
                
                # Clean-up ot the words not referenced anywhere
                for author in models.Author.objects.all():
                    if not models.Book.objects.filter(author=author):
                        author.delete()
                
                return HttpResponseRedirect(reverse('list_book'))
        
        return self.get(request)

class CreateUpdateTranslationView(LoginRequiredMixin,View):

    def initalize_nested_fields(self):
        self.nested_fields = []
        self.nested_fields.append(TranslationForeignKeyTranslationField(model_name="Word",model_form_name="WordForm",field_autocomplete_name="word",user_based=False))

    def get(self, request, slug=None, slug_book=None):
    
        # Getting nested_fields
        self.initalize_nested_fields()
        
        # Getting pre-instance
        pre_instance = models.Translation.objects.filter(slug=slug).first()
        
        # Creating a new form
        if pre_instance is None:
            form = forms.TranslationForm()
        else:
            form = forms.TranslationForm(instance=pre_instance)
        variables_dict = {'form':form,'slug':slug,'slug_book':slug_book,'target_input_words':""}
        
        # Creating nested forms
        for field in self.nested_fields:
            field.initialize_get(request,pre_instance)
            field.update_variables_dict(variables_dict)
          
        return render(request, 'dictionary/vocform.html', variables_dict)

    def post(self, request, slug=None, slug_book=None):
    
        # Initialize main form
        pre_instance = models.Translation.objects.filter(slug=slug).first()
        
        if pre_instance is None:
            form = forms.TranslationForm(request.POST)
            update = False
        else:
            form = forms.TranslationForm(request.POST,instance=pre_instance)
            update = True
    
        # Getting nested_fields
        self.initalize_nested_fields()
        
        success = True
        for field in self.nested_fields:
            success = field.initialize_post(request)
            if not success:
                break
        
        if success:
            
            if form.is_valid():
                translate = form.save(commit=False)
                for field in self.nested_fields:
                    field.update_main_form(translate)
                translate.user = request.user
                translate_item = translate.save()
                
                # Clean-up ot the words not referenced anywhere
                for word in models.Word.objects.all():
                    if not models.Translation.objects.filter(Q(original_word=word)|Q(translated_word=word)):
                        word.delete()
                
                if slug_book is not None:
                    if not update:
                        book = get_object_or_404(models.Book, slug=slug_book)
                        translation_link = models.TranslationLink()
                        translation_link.item = translate
                        translation_link.book = book
                        id_translationlink = translation_link.save()
                        
                    return HttpResponseRedirect(reverse('details_book', kwargs={'slug_book':slug_book}))
                    
                return HttpResponseRedirect(reverse('list_translations'))
                
            else:
                print("Error main form")
                print(form.errors)
                
        else:
            print("Adding words has not worked")
    
        return self.get(request)
   
class BooksListView(LoginRequiredMixin,ListView):

    model = models.Book
    paginate_by = 10  # if pagination is desired
    template_name = "dictionary/books_list.html"
    
    def get_queryset(self):
        return models.Book.objects.filter(user=self.request.user)

class TranslationListView(LoginRequiredMixin,ListView):

    model = models.Translation
    paginate_by = 10  # if pagination is desired
    template_name = "dictionary/translation_list.html"
     
    def get_queryset(self):
        return models.Translation.objects.filter(user=self.request.user)

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
        
class DeleteTranslationView(DeleteView):
    model = models.Translation
    slug_url_kwarg = 'slug'
    template_name = 'dictionary/confirm_delete.html'
    
    def get_object(self):
        return get_object_or_404(models.Translation,slug=self.kwargs['slug'])
        
    def get_success_url(self):
        if "slug_book" in self.kwargs:
            return reverse('details_book', kwargs={'slug_book':self.kwargs['slug_book']})
        else:
            return reverse('list_translations')
            
class DeleteBookView(DeleteView):
    model = models.Book
    slug_url_kwarg = 'slug_book'
    template_name = 'dictionary/confirm_delete.html'
    
    def get_object(self):
        return get_object_or_404(models.Book,slug=self.kwargs['slug_book'])
        
    def get_success_url(self):
        return reverse('list_book')
        
    