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

class CreateUpdateBookView(LoginRequiredMixin,AutoCompletionView):

    def __init__(self):
        model = models.Book
        model_form = forms.BookForm
        main_slug_name = "slug_book"
        slugs_list = []
        template_path = 'dictionary/bookform.html'
        nested_fields = []
        nested_fields.append(AutoCompletionNestedField(model_name="Author",model_form_name="AuthorForm",field_autocomplete_name="first_name",prefix="author",title="Author",user_based=False))
        AutoCompletionView.__init__(self,model=model,model_form=model_form,main_slug_name=main_slug_name,slugs_list=slugs_list,template_path=template_path,nested_fields=nested_fields)        

    def set_slug_user(self, request):
        self.item.user = request.user
        self.item.slug = slugify(self.item.title)
        
    def clean_useless_records(self):
        for author in models.Author.objects.all():
            if not models.Book.objects.filter(author=author):
                author.delete()
        
    def redirect_success(self,request,**kwargs):
        return HttpResponseRedirect(reverse('list_book'))
        
    def redirect_fail(self,request,**kwargs):
        return self.get(request)
        
class CreateUpdateTranslationView(LoginRequiredMixin,AutoCompletionView):

    def __init__(self):
        model = models.Translation
        model_form = forms.TranslationForm
        main_slug_name = "slug"
        slugs_list = ["slug_book"]
        template_path = 'dictionary/vocform.html'
        nested_fields = []
        nested_fields.append(AutoCompletionNestedField(model_name="Word",model_form_name="WordForm",field_autocomplete_name="word",prefix="original_word",title="Original word",user_based=False))
        nested_fields.append(AutoCompletionNestedField(model_name="Word",model_form_name="WordForm",field_autocomplete_name="word",prefix="translated_word",title="Translated word",user_based=False))
        AutoCompletionView.__init__(self,model=model,model_form=model_form,main_slug_name=main_slug_name,slugs_list=slugs_list,template_path=template_path,nested_fields=nested_fields)        

    def set_slug_user(self, request):
        self.item.user = request.user
        self.item.slug = slugify(self.nested_fields[0].item.__str__() + "-" + self.nested_fields[1].item.__str__())
        
    def clean_useless_records(self):
        for word in models.Word.objects.all():
            if not models.Translation.objects.filter(Q(original_word=word)|Q(translated_word=word)):
                word.delete()
        
    def post_save(self,update,**kwargs):
        if "slug_book" in kwargs:
            if not update:
                book = get_object_or_404(models.Book, slug=kwargs['slug_book'])
                translation_link = models.TranslationLink()
                translation_link.item = self.item
                translation_link.book = book
                id_translationlink = translation_link.save()
                
            return HttpResponseRedirect(reverse('details_book', kwargs={'slug_book':kwargs['slug_book']}))
        
    def redirect_success(self,request,**kwargs):
        return HttpResponseRedirect(reverse('list_translations'))
        
    def redirect_fail(self,request,**kwargs):
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
        
    