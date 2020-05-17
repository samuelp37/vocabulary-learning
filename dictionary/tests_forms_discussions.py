from django.test import RequestFactory, TestCase
from . import forms
import factory
from . import factories

# class TestAddAuthorForm(TestCase) > already tested in test_forms_books

class TestAddUpdateDiscussionForm(TestCase):

    def test_DiscussionForm_valid(self):
        form = forms.DiscussionForm(data={'title':factory.Faker('sentence'),'language':factories.LanguageFactory.create().pk})
        self.assertTrue(form.is_valid())

    def test_DiscussionForm_missing(self):
        form = forms.DiscussionForm(data={'title':'','language':factories.LanguageFactory.create().pk})
        self.assertFalse(form.is_valid())

        form = forms.DiscussionForm(data={'title':'','language':''})
        self.assertFalse(form.is_valid())

        form = forms.DiscussionForm(data={'title':factory.Faker('sentence'),'language':''})
        self.assertFalse(form.is_valid())
