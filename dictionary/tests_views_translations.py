from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
from .views import *
from . import models
from django.urls import reverse
import factory
from . import factories
from .tests_commons import *
import datetime

# Creation view for Translations
class TestCreateTranslationView(TestCase):
    """
    Translation creation view
    """

    url_name="add"
    slug_parameter_name=None
    support_model=None # models.Translation
    support_model_factory=None
    url_success_slug=None # "details_book"
    support_translation_joint=None # models.TranslationLink

    def populate_post_request(self):
        
        # Creatng a POST request
        self.request.POST = self.request.POST.copy()

        self.request.POST['original_word-word'] = factory.Faker('word').generate({})[:70]
        self.request.POST['original_word-gender'] = factories.GenderFactory.create().pk
        self.request.POST['original_word-language'] = factories.LanguageFactory.create().pk

        self.request.POST['translated_word-word'] = factory.Faker('word').generate({})[:70]
        self.request.POST['translated_word-gender'] = factories.GenderFactory.create().pk
        self.request.POST['translated_word-language'] = factories.LanguageFactory.create().pk

        self.request.POST['original_adj-word'] = factory.Faker('word').generate({})[:70]
        self.request.POST['original_adj-language'] = factories.LanguageFactory.create().pk    

        self.request.POST['translated_adj-word'] = factory.Faker('word').generate({})[:70]
        self.request.POST['translated_adj-language'] = factories.LanguageFactory.create().pk 

        self.request.POST['original_verb-word'] = factory.Faker('word').generate({})[:70]
        self.request.POST['original_verb-language'] = factories.LanguageFactory.create().pk    

        self.request.POST['translated_verb-word'] = factory.Faker('word').generate({})[:70]
        self.request.POST['translated_verb-language'] = factories.LanguageFactory.create().pk

        self.request.POST['original_exp-expression'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['original_exp-language'] = factories.LanguageFactory.create().pk    

        self.request.POST['translated_exp-expression'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['translated_exp-language'] = factories.LanguageFactory.create().pk

        self.request.POST['date_added'] = datetime.datetime.now().date()


    def populate_invalid_request(self):

        # Creatng a POST request
        self.request.POST = self.request.POST.copy()

        self.request.POST['original_word-word'] = factory.Faker('word').generate({})[:70]
        self.request.POST['original_word-gender'] = factories.GenderFactory.create().pk
        self.request.POST['original_word-language'] = factories.LanguageFactory.create().pk

        self.request.POST['translated_word-word'] = ''
        self.request.POST['translated_word-gender'] = factories.GenderFactory.create().pk
        self.request.POST['translated_word-language'] = factories.LanguageFactory.create().pk

        self.request.POST['original_adj-word'] = ''
        self.request.POST['original_adj-language'] = factories.LanguageFactory.create().pk    

        self.request.POST['translated_adj-word'] = ''
        self.request.POST['translated_adj-language'] = factories.LanguageFactory.create().pk 

        self.request.POST['original_verb-word'] = ''
        self.request.POST['original_verb-language'] = factories.LanguageFactory.create().pk    

        self.request.POST['translated_verb-word'] = factory.Faker('word').generate({})[:70]
        self.request.POST['translated_verb-language'] = factories.LanguageFactory.create().pk

        self.request.POST['original_exp-expression'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['original_exp-language'] = factories.LanguageFactory.create().pk    

        self.request.POST['translated_exp-expression'] = ''
        self.request.POST['translated_exp-language'] = factories.LanguageFactory.create().pk

        self.request.POST['date_added'] = datetime.datetime.now().date()

    def setUp(self):

        self.factory = RequestFactory()
        if self.slug_parameter_name is None:
            self.request = self.factory.get(reverse(self.url_name))
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
            self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))

        # Populate the database with some existing books
        for _ in range(7):
            factories.TranslationFactory.create()

        self.translations_count = models.Translation.objects.count()
        if self.support_translation_joint is not None:
            self.translations_support_count = self.support_translation_joint.objects.count()

    def test_create_translation_anonymous(self):
        """
        TEST : Get the translation creation form without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        self.request.user = AnonymousUser()
        if self.slug_parameter_name is None:
            response = CreateUpdateTranslationView.as_view()(self.request)
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
            response =  CreateUpdateTranslationView.as_view()(self.request,**kwargs)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_post_create_translation_anonymous(self):
        """
        TEST : Get the translation creation form without being logged
        Behavior expected : Redirection to the login page
        """

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        if self.slug_parameter_name is None:
            self.request = self.factory.post(reverse(self.url_name))
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
            self.request = self.factory.post(reverse(self.url_name,kwargs=kwargs))
        self.request.user = AnonymousUser()

        # Populate POST request
        self.populate_post_request()

        if self.slug_parameter_name is None:
            response = CreateUpdateTranslationView.as_view()(self.request)
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
            response =  CreateUpdateTranslationView.as_view()(self.request,**kwargs)

        # Assert no translation has been created
        self.assertEqual(models.Translation.objects.count(),self.translations_count)
        if self.support_translation_joint is not None:
            self.assertEqual(self.support_translation_joint.objects.count(),self.translations_support_count)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)     

    def test_get_create_translation_logged(self):
        """
        TEST : Get the translation creation form while being logged
        Behavior expected : The user should access the translation creation page
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        self.request.user = user

        # Executing a HTTP request towards the page
        if self.slug_parameter_name is None:
            response = CreateUpdateTranslationView.as_view()(self.request)
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
            response =  CreateUpdateTranslationView.as_view()(self.request,**kwargs)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)

    def test_post_create_translation_logged_noword(self):
        """
        TEST : Executing a POST request to create a translation while omitting to specify a complete translation
        Behavior expected : No translation neither words should be created and the user should be redirected back to the discussion creation form.
        """

        # Create a fake user
        user = factories.UserFactory.create()

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        if self.slug_parameter_name is None:
            self.request = self.factory.post(reverse(self.url_name))
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
            self.request = self.factory.post(reverse(self.url_name,kwargs=kwargs))
        self.request.user = user

        # Creating a POST request
        self.populate_invalid_request()

        # Executing the request
        if self.slug_parameter_name is None:
            response = CreateUpdateTranslationView.as_view()(self.request)
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
            response =  CreateUpdateTranslationView.as_view()(self.request,**kwargs)

        # Assert no translation has been created
        self.assertEqual(models.Translation.objects.count(),self.translations_count)
        if self.support_translation_joint is not None:
            self.assertEqual(self.support_translation_joint.objects.count(),self.translations_support_count)

        # Checking whether the page is unchanged and the user is reaching again the translation creation form
        self.assertEqual(response.status_code, 200)

    def test_post_create_translation_logged_valid(self):
        """
        TEST : Executing a POST request to create a translation that is valid (all categories triggered)
        Behavior expected : A translation should be created and the user should be redirected
        """

        # Create a fake user
        user = factories.UserFactory.create()

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        if self.slug_parameter_name is None:
            self.request = self.factory.post(reverse(self.url_name))
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {}
            kwargs[self.slug_parameter_name]=support_ex.slug
            self.request = self.factory.post(reverse(self.url_name,kwargs=kwargs))
        self.request.user = user

        # Creating a POST request
        self.populate_post_request()

        # Executing the request
        if self.slug_parameter_name is None:
            response = CreateUpdateTranslationView.as_view()(self.request)
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
            response =  CreateUpdateTranslationView.as_view()(self.request,**kwargs)

        # Assert a translation has been created
        self.assertEqual(models.Translation.objects.count(),self.translations_count+1)
        if self.support_translation_joint is not None:
            self.assertEqual(self.support_translation_joint.objects.count(),self.translations_support_count+1)

            # Checking the joint has been created
            last_joint = self.support_translation_joint.objects.latest('pk')
            last_translation = models.Translation.objects.latest('pk')
            self.assertEqual(last_joint.item,last_translation)
            self.assertEqual(getattr(last_joint,self.joint_support_name),support_ex)

        # Checking whether the user is redirected
        self.assertEqual(response.status_code, 302)
        if self.slug_parameter_name and self.url_success_slug:
            self.assertEqual(response.url, reverse(self.url_success_slug,kwargs=kwargs))
        else:
            self.assertEqual(response.url, reverse('list_translations'))

class TestCreateTranslationViewBookSupport(TestCreateTranslationView):
    """
    Translation creation view - Book support
    """

    url_name="add_word_book"
    slug_parameter_name="slug_book"
    support_model=models.Book
    support_model_factory=factories.BookFactory
    url_success_slug="details_book"
    support_translation_joint=models.TranslationLink
    joint_support_name='book'

class TestCreateTranslationViewDiscussionSupport(TestCreateTranslationView):
    """
    Translation creation view - Discussion support
    """

    url_name="add_word_discussion"
    slug_parameter_name="slug_discussion"
    support_model=models.Discussion
    support_model_factory=factories.DiscussionFactory
    url_success_slug="details_discussion"
    support_translation_joint=models.TranslationLinkDiscussion
    joint_support_name='discussion'

class TestCreateTranslationViewArticleSupport(TestCreateTranslationView):
    """
    Translation creation view - Article support
    """

    url_name="add_word_article"
    slug_parameter_name="slug_article"
    support_model=models.Article
    support_model_factory=factories.ArticleFactory
    url_success_slug="details_article"
    support_translation_joint=models.TranslationLinkArticle
    joint_support_name='article'