from django.test import RequestFactory, TestCase
from . import forms
import factory
from . import factories

class TestAddNewspaperForm(TestCase):
    
    def test_NewspaperForm_valid(self):
        form = forms.NewspaperForm(data={'name':factory.Faker('word')})
        self.assertTrue(form.is_valid())

    def test_NeswpaperForm_missing(self):
        form = forms.AuthorForm(data={'name':''})
        self.assertFalse(form.is_valid())

class TestAddTopicForm(TestCase):
    
    def test_TopicForm_valid(self):
        form = forms.TopicForm(data={'name':factory.Faker('word')})
        self.assertTrue(form.is_valid())

    def test_TopicForm_missing(self):
        form = forms.TopicForm(data={'name':''})
        self.assertFalse(form.is_valid())

class TestAddUpdateArticleForm(TestCase):

    def test_ArticleForm_valid(self):
        form = forms.ArticleForm(data={'title':factory.Faker('sentence'),'language':factories.LanguageFactory.create().pk})
        self.assertTrue(form.is_valid())

    def test_ArticleForm_missing(self):
        form = forms.ArticleForm(data={'title':'','language':factories.LanguageFactory.create().pk})
        self.assertFalse(form.is_valid())

        form = forms.ArticleForm(data={'title':'','language':''})
        self.assertFalse(form.is_valid())

        form = forms.ArticleForm(data={'title':factory.Faker('sentence'),'language':''})
        self.assertFalse(form.is_valid())
