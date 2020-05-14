from django.test import RequestFactory, TestCase
from . import forms
import factory
from . import factories

class TestAddAuthorForm(TestCase):
    
    def test_AuthorForm_valid(self):
        form = forms.AuthorForm(data={'first_name':factory.Faker('first_name'),'last_name':factory.Faker('last_name')})
        self.assertTrue(form.is_valid())

    def test_AuthorForm_missing(self):
        form = forms.AuthorForm(data={'first_name':'','last_name':factory.Faker('last_name')})
        self.assertFalse(form.is_valid())

        form = forms.AuthorForm(data={'first_name':'','last_name':''})
        self.assertFalse(form.is_valid())

        form = forms.AuthorForm(data={'first_name':factory.Faker('first_name'),'last_name':''})
        self.assertFalse(form.is_valid())

class TestAddUpdateBookForm(TestCase):

    def test_BookForm_valid(self):
        form = forms.BookForm(data={'title':factory.Faker('sentence'),'language':factories.LanguageFactory.create().pk})
        self.assertTrue(form.is_valid())

    def test_BookForm_missing(self):
        form = forms.BookForm(data={'title':'','language':factories.LanguageFactory.create().pk})
        self.assertFalse(form.is_valid())

        form = forms.BookForm(data={'title':'','language':''})
        self.assertFalse(form.is_valid())

        form = forms.BookForm(data={'title':factory.Faker('sentence'),'language':''})
        self.assertFalse(form.is_valid())
