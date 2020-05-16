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
import sys
from django.db.models import Q

from .views_common import *
import datetime

class HomeNoMemberView(TemplateView):

    template_name = 'dictionary/home_nomember.html'

class HomeMemberView(LoginRequiredMixin,TemplateView):

    template_name = 'dictionary/home_member.html'
    
class WordAutocompleteView(LoginRequiredMixin,View,AutoCompletionNestedField):

    def __init__(self):
        AutoCompletionNestedField.__init__(self,model_name="Word",model_form_name="WordForm",field_autocomplete_name="word",prefix=None,title=None,user_based=False)
        
class AdjectiveAutocompleteView(LoginRequiredMixin,View,AutoCompletionNestedField):

    def __init__(self):
        AutoCompletionNestedField.__init__(self,model_name="Adjective",model_form_name="AdjectiveForm",field_autocomplete_name="word",prefix=None,title=None,user_based=False)
        
class VerbAutocompleteView(LoginRequiredMixin,View,AutoCompletionNestedField):

    def __init__(self):
        AutoCompletionNestedField.__init__(self,model_name="Verb",model_form_name="VerbForm",field_autocomplete_name="word",prefix=None,title=None,user_based=False)

class AuthorAutocompleteView(LoginRequiredMixin,View,AutoCompletionNestedField):

    def __init__(self):
        AutoCompletionNestedField.__init__(self,model_name="Author",model_form_name="AuthorForm",field_autocomplete_name="first_name",prefix=None,title=None,user_based=False)

class NewspaperAutocompleteView(LoginRequiredMixin,View,AutoCompletionNestedField):

    def __init__(self):
        AutoCompletionNestedField.__init__(self,model_name="Newspaper",model_form_name="NewspaperForm",field_autocomplete_name="name",prefix=None,title=None,user_based=False)

class TopicAutocompleteView(LoginRequiredMixin,View,AutoCompletionNestedField):

    def __init__(self):
        AutoCompletionNestedField.__init__(self,model_name="Topic",model_form_name="TopicForm",field_autocomplete_name="name",prefix=None,title=None,user_based=False)

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
        self.item.slug = slugify(self.item.title + "-" + random_str(15))
        
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
        self.models_access_list = model.get_model_access_list()
        model_form = forms.TranslationForm
        main_slug_name = "slug"
        slugs_list = [model.extern_slug() for model in self.models_access_list]
        template_path = 'dictionary/vocform.html'
        nested_fields = []
        nested_fields.append(AutoCompletionNestedField(model_name="Word",model_form_name="WordForm",field_autocomplete_name="word",prefix="original_word",title="Original name",user_based=False))
        nested_fields.append(AutoCompletionNestedField(model_name="Word",model_form_name="WordForm",field_autocomplete_name="word",prefix="translated_word",title="Translated name",user_based=False))
        nested_fields.append(AutoCompletionNestedField(model_name="Adjective",model_form_name="AdjectiveForm",field_autocomplete_name="word",prefix="original_adj",title="Original adjective",user_based=False))
        nested_fields.append(AutoCompletionNestedField(model_name="Adjective",model_form_name="AdjectiveForm",field_autocomplete_name="word",prefix="translated_adj",title="Translated adjective",user_based=False))
        nested_fields.append(AutoCompletionNestedField(model_name="Verb",model_form_name="VerbForm",field_autocomplete_name="word",prefix="original_verb",title="Original verb",user_based=False))
        nested_fields.append(AutoCompletionNestedField(model_name="Verb",model_form_name="VerbForm",field_autocomplete_name="word",prefix="translated_verb",title="Translated verb",user_based=False))
        nested_fields.append(AutoCompletionNestedField(model_name="Expression",model_form_name="ExpressionForm",field_autocomplete_name=None,prefix="original_exp",title="Original expression",user_based=False))
        nested_fields.append(AutoCompletionNestedField(model_name="Expression",model_form_name="ExpressionForm",field_autocomplete_name=None,prefix="translated_exp",title="Translated expression",user_based=False))
        
        AutoCompletionView.__init__(self,model=model,model_form=model_form,main_slug_name=main_slug_name,slugs_list=slugs_list,template_path=template_path,nested_fields=nested_fields)        

    def set_slug_user(self, request):
        self.item.user = request.user
        self.item.slug = slugify("-".join([field.item.__str__()[:30] for field in self.nested_fields]) + "-" +   random_str(15))
        
    def custom_nested_fields_handler(self,request):
        """
        Special for this particular case : the user can choose to il la subset of {name,adjective,verb,expression} not empty.
        Each one of this option is represented by two autocomplete fields
        """
        success = False
        for i in range(int(len(self.nested_fields)/2)):
            field_0, field_1 = self.nested_fields[i*2],self.nested_fields[i*2+1]
            bool_field0 = field_0.initialize_post(request)
            bool_field1 = field_1.initialize_post(request)
            if bool_field0 and bool_field1:
                success = True
        return success
        
    def clean_useless_records(self):
        for word in models.Word.objects.all():
            if not models.Translation.objects.filter(Q(original_word=word)|Q(translated_word=word)):
                word.delete()
        for adj in models.Adjective.objects.all():
            if not models.Translation.objects.filter(Q(original_adj=adj)|Q(translated_adj=adj)):
                adj.delete()
        for verb in models.Verb.objects.all():
            if not models.Translation.objects.filter(Q(original_verb=verb)|Q(translated_verb=verb)):
                verb.delete()
        for exp in models.Expression.objects.all():
            if not models.Translation.objects.filter(Q(original_exp=exp)|Q(translated_exp=exp)):
                exp.delete()
        
    def post_save(self,update,**kwargs):
        
        model_chosen = get_model_chosen(self.models_access_list,kwargs)
        if model_chosen is None:
            return None
        
        dict = model_chosen.translation_utils()
        if not update:
            item_support = get_object_or_404(model_chosen, slug=kwargs[model_chosen.extern_slug()])
            translation_link = dict["model_link"]
            translation_link.item = self.item
            setattr(translation_link,dict["model_link_attr"],item_support)
            id_translationlink = translation_link.save()
        return HttpResponseRedirect(reverse('details_'+dict["model_link_attr"], kwargs={model_chosen.extern_slug():kwargs[model_chosen.extern_slug()]}))
        
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
    
class BookView(LoginRequiredMixin,AuthorizeAccessDetailView,DetailView):

    model = models.Book
    template_name = 'dictionary/book_detail.html'
    slug_url_kwarg = 'slug_book'
        
class TranslationView(LoginRequiredMixin,AuthorizeAccessDetailView,DetailView):

    model = models.Translation
    template_name = 'dictionary/translation_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'translation'
        
    def get_context_data(self, **kwargs):
        context = super(TranslationView, self).get_context_data(**kwargs)
        
        model_chosen = get_model_chosen(self.model.get_model_access_list(),self.kwargs)
        if model_chosen is None:
            return context
        
        context[model_chosen.extern_slug()] = model_chosen.extern_slug()
        return context
        
class DeleteTranslationView(AuthorizeAccessDetailView,DeleteView):
    model = models.Translation
    slug_url_kwarg = 'slug'
    template_name = 'dictionary/confirm_delete.html'
        
    def get_success_url(self):
    
        model_chosen = get_model_chosen(self.model.get_model_access_list(),self.kwargs)
        if model_chosen is None:
            return reverse('list_translations')
        else:
            dict = model_chosen.translation_utils()
            return reverse('details_'+dict["model_link_attr"], kwargs={model_chosen.extern_slug():self.kwargs[model_chosen.extern_slug()]})
            
class DeleteBookView(LoginRequiredMixin,AuthorizeAccessDetailView,DeleteView):
    model = models.Book
    slug_url_kwarg = 'slug_book'
    template_name = 'dictionary/confirm_delete.html'
        
    def get_success_url(self):
        return reverse('list_book')
        
# Articles

class ArticlesListView(LoginRequiredMixin,ListView):

    model = models.Article
    paginate_by = 10  # if pagination is desired
    template_name = "dictionary/articles_list.html"
    
    def get_queryset(self):
        return models.Article.objects.filter(user=self.request.user)
        
class CreateUpdateArticleView(LoginRequiredMixin,AutoCompletionView):

    def __init__(self):
        model = models.Article
        model_form = forms.ArticleForm
        main_slug_name = "slug_article"
        slugs_list = []
        template_path = 'dictionary/articleform.html'
        nested_fields = []
        nested_fields.append(AutoCompletionNestedField(model_name="Topic",model_form_name="TopicForm",field_autocomplete_name="name",prefix="topic",title="Topic",user_based=False))
        nested_fields.append(AutoCompletionNestedField(model_name="Newspaper",model_form_name="NewspaperForm",field_autocomplete_name="name",prefix="newspaper",title="Newspaper",user_based=False))
        AutoCompletionView.__init__(self,model=model,model_form=model_form,main_slug_name=main_slug_name,slugs_list=slugs_list,template_path=template_path,nested_fields=nested_fields)        

    def set_slug_user(self, request):
        self.item.user = request.user
        self.item.slug = slugify(self.item.title + self.item.newspaper.name  + "-" + random_str(15))
        
    def clean_useless_records(self):
        for newspaper in models.Newspaper.objects.all():
            if not models.Article.objects.filter(newspaper=newspaper):
                newspaper.delete()
        
    def redirect_success(self,request,**kwargs):
        return HttpResponseRedirect(reverse('list_article'))
        
    def redirect_fail(self,request,**kwargs):
        return self.get(request)
        
class ArticleView(LoginRequiredMixin,AuthorizeAccessDetailView,DetailView):

    model = models.Article
    template_name = 'dictionary/article_detail.html'
    slug_url_kwarg = 'slug_article'
        
class DeleteArticleView(AuthorizeAccessDetailView,DeleteView):
    model = models.Article
    slug_url_kwarg = 'slug_article'
    template_name = 'dictionary/confirm_delete.html'
        
    def get_success_url(self):
        return reverse('list_article')
        

# Discussions

class DiscussionsListView(LoginRequiredMixin,ListView):

    model = models.Discussion
    paginate_by = 10  # if pagination is desired
    template_name = "dictionary/discussions_list.html"
    
    def get_queryset(self):
        return models.Discussion.objects.filter(user=self.request.user)
        
class CreateUpdateDiscussionView(LoginRequiredMixin,AutoCompletionView):

    def __init__(self):
        model = models.Discussion
        model_form = forms.DiscussionForm
        main_slug_name = "slug_discussion"
        slugs_list = []
        template_path = 'dictionary/discussionform.html'
        nested_fields = []
        nested_fields.append(AutoCompletionNestedField(model_name="Topic",model_form_name="TopicForm",field_autocomplete_name="name",prefix="topic",title="Topic",user_based=False))
        AutoCompletionView.__init__(self,model=model,model_form=model_form,main_slug_name=main_slug_name,slugs_list=slugs_list,template_path=template_path,nested_fields=nested_fields)        

    def set_slug_user(self, request):
        self.item.user = request.user
        self.item.slug = slugify(self.item.title + "-" + self.item.topic.name + "-" + random_str(15))
        
    def clean_useless_records(self):
        pass
        
    def redirect_success(self,request,**kwargs):
        return HttpResponseRedirect(reverse('list_discussion'))
        
    def redirect_fail(self,request,**kwargs):
        return self.get(request)
        
class DiscussionView(LoginRequiredMixin,AuthorizeAccessDetailView,DetailView):

    model = models.Discussion
    template_name = 'dictionary/discussion_detail.html'
    slug_url_kwarg = 'slug_discussion'
        
class DeleteDiscussionView(LoginRequiredMixin,AuthorizeAccessDetailView,DeleteView):
    model = models.Discussion
    slug_url_kwarg = 'slug_discussion'
    template_name = 'dictionary/confirm_delete.html'
        
    def get_success_url(self):
        return reverse('list_discussion')
        
# Quizz

class CreateReviewView(LoginRequiredMixin,View):

    def __init__(self):
        self.model = models.Quizz
        self.model_form = forms.QuizzForm
        self.template_path = 'dictionary/quizzform.html'

    def get(self, request):
        return render(request, self.template_path, {'form':self.model_form()})

    def post(self, request):
    
        form = self.model_form(request.POST)
        
        number_questions = int(request.POST['number_questions'])
        if 'original_to_translated' in request.POST:
            original_to_translated = True
        else:
            original_to_translated = False
        user = request.user
        date_quizz = datetime.date.today()
        slug = slugify("Quizz-" + date_quizz.strftime("%d/%m/%Y") + "-" + random_str(15))
        ordering_policy = request.POST['ordering_policy']
        
        quizz_instance = models.Quizz(slug=slug, date_quizz=date_quizz,user=user)
        quizz_instance.save()
        
        if ordering_policy=="random":
            translations_list = models.Translation.objects.all().order_by('?')[:number_questions]
        else:
            raise Exception("Not implemented yet")
        
        for translation in translations_list:
            slug = "quizz_item_"+random_str(40)
            quizz_item = models.QuizzItem(translation = translation,original_to_translate = original_to_translated,delivered_on=None,delta_reply=None,slug=slug,success=None)
            quizz_item.save()
            quizz_link = models.QuizzLinkItem(quizz=quizz_instance,quizz_item=quizz_item)
            quizz_link.save()
        
        return HttpResponseRedirect(reverse('quizz_review_item', kwargs={'slug_item':quizz_item.slug,'slug_review':quizz_instance.slug}))
        
class QuizzReviewItemView(LoginRequiredMixin,AuthorizeAccessDetailView,DetailView):

    model = models.QuizzItem
    template_name = 'dictionary/quizzitem_detail.html'
    slug_url_kwarg = 'slug_item'
    
    def get_object(self):
        quizz_item = super().get_object()
        quizz_item.delivered_on = datetime.datetime.now(datetime.timezone.utc)
        quizz_item.save()
        return quizz_item
        
    def get_context_data(self, **kwargs):
        context = super(QuizzReviewItemView, self).get_context_data(**kwargs)
        context['slug_review'] = self.kwargs['slug_review']
        
        if context['object'].original_to_translate:
            context['object'].original_blurred = ""
            context['object'].translate_blurred = "blurred"
        else:
            context['object'].original_blurred = "blurred"
            context['object'].translate_blurred = ""
        
        return context
        
class QuizzAnalysisReviewItemView(LoginRequiredMixin,AuthorizeAccessDetailView,View):
    
    model = models.Quizz
    slug_url_kwarg = 'slug_review'
    
    def get(self, request, **kwargs):
        
        slug_quizz = self.kwargs['slug_review']
        slug_item = self.kwargs['slug_item']
        success = (int(self.kwargs['success']) != 0)
        
        quizz_item = get_object_or_404(models.QuizzItem,slug=slug_item)
        quizz = get_object_or_404(models.Quizz,slug=slug_quizz)
        
        current_datetime = datetime.datetime.now(datetime.timezone.utc)
        delta_datetime = current_datetime-quizz_item.delivered_on
        delta_reply_seconds = delta_datetime.total_seconds()
        
        quizz_item.success = success
        quizz_item.delta_reply = delta_reply_seconds
        quizz_item.save()
        
        next_quizz_item = quizz.items.all().filter(success=None).first()
        print(next_quizz_item)
        
        if next_quizz_item is not None:
            return HttpResponseRedirect(reverse('quizz_review_item', kwargs={'slug_item':next_quizz_item.slug,'slug_review':quizz.slug}))
        
        return HttpResponseRedirect(reverse('details_review', kwargs={'slug_review':quizz.slug}))
        
class ResumeReviewView(LoginRequiredMixin,AuthorizeAccessDetailView,View):
    
    model = models.Quizz
    slug_url_kwarg = 'slug_review'
    
    def get(self, request, **kwargs):
        
        slug_quizz = self.kwargs[self.slug_url_kwarg]
        quizz = get_object_or_404(self.model,slug=slug_quizz)
        
        next_quizz_item = quizz.items.all().filter(success=None).first()
        print(next_quizz_item)
        
        if next_quizz_item is not None:
            return HttpResponseRedirect(reverse('quizz_review_item', kwargs={'slug_item':next_quizz_item.slug,'slug_review':quizz.slug}))
        
        return HttpResponseRedirect(reverse('details_review', kwargs={'slug_review':quizz.slug}))

class ReviewsListView(LoginRequiredMixin,ListView):

    model = models.Quizz
    paginate_by = 10  # if pagination is desired
    template_name = "dictionary/quizz_list.html"
    ordering = ['-date_quizz','-id']
    
    def get_queryset(self):
        return models.Quizz.objects.filter(user=self.request.user).order_by(self.ordering[0],self.ordering[1])
        
class ReviewView(LoginRequiredMixin,AuthorizeAccessDetailView,DetailView):

    model = models.Quizz
    template_name = 'dictionary/review_detail.html'
    slug_url_kwarg = 'slug_review'
        
class DeleteReviewView(AuthorizeAccessDetailView,DeleteView):
    model = models.Quizz
    slug_url_kwarg = 'slug_review'
    template_name = 'dictionary/confirm_delete.html'
        
    def get_success_url(self):
        return reverse('list_reviews')