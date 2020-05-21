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

    @staticmethod
    def populate_post_request(request):
        
        # Creatng a POST request
        request.POST = request.POST.copy()

        request.POST['original_word-word'] = factory.Faker('word').generate({})[:70]
        request.POST['original_word-gender'] = factories.GenderFactory.create().pk
        request.POST['original_word-language'] = factories.LanguageFactory.create().pk

        request.POST['translated_word-word'] = factory.Faker('word').generate({})[:70]
        request.POST['translated_word-gender'] = factories.GenderFactory.create().pk
        request.POST['translated_word-language'] = factories.LanguageFactory.create().pk

        request.POST['original_adj-word'] = factory.Faker('word').generate({})[:70]
        request.POST['original_adj-language'] = factories.LanguageFactory.create().pk    

        request.POST['translated_adj-word'] = factory.Faker('word').generate({})[:70]
        request.POST['translated_adj-language'] = factories.LanguageFactory.create().pk 

        request.POST['original_verb-word'] = factory.Faker('word').generate({})[:70]
        request.POST['original_verb-language'] = factories.LanguageFactory.create().pk    

        request.POST['translated_verb-word'] = factory.Faker('word').generate({})[:70]
        request.POST['translated_verb-language'] = factories.LanguageFactory.create().pk

        request.POST['original_exp-expression'] = factory.Faker('sentence').generate({})[:70]
        request.POST['original_exp-language'] = factories.LanguageFactory.create().pk    

        request.POST['translated_exp-expression'] = factory.Faker('sentence').generate({})[:70]
        request.POST['translated_exp-language'] = factories.LanguageFactory.create().pk

        request.POST['date_added'] = datetime.datetime.now().date()

    @staticmethod
    def populate_invalid_request(request):

        # Creatng a POST request
        request.POST = request.POST.copy()

        request.POST['original_word-word'] = factory.Faker('word').generate({})[:70]
        request.POST['original_word-gender'] = factories.GenderFactory.create().pk
        request.POST['original_word-language'] = factories.LanguageFactory.create().pk

        request.POST['translated_word-word'] = ''
        request.POST['translated_word-gender'] = factories.GenderFactory.create().pk
        request.POST['translated_word-language'] = factories.LanguageFactory.create().pk

        request.POST['original_adj-word'] = ''
        request.POST['original_adj-language'] = factories.LanguageFactory.create().pk    

        request.POST['translated_adj-word'] = ''
        request.POST['translated_adj-language'] = factories.LanguageFactory.create().pk 

        request.POST['original_verb-word'] = ''
        request.POST['original_verb-language'] = factories.LanguageFactory.create().pk    

        request.POST['translated_verb-word'] = factory.Faker('word').generate({})[:70]
        request.POST['translated_verb-language'] = factories.LanguageFactory.create().pk

        request.POST['original_exp-expression'] = factory.Faker('sentence').generate({})[:70]
        request.POST['original_exp-language'] = factories.LanguageFactory.create().pk    

        request.POST['translated_exp-expression'] = ''
        request.POST['translated_exp-language'] = factories.LanguageFactory.create().pk

        request.POST['date_added'] = datetime.datetime.now().date()

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
            kwargs = {}
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
            self.request = self.factory.post(reverse(self.url_name,kwargs=kwargs))
        self.request.user = AnonymousUser()

        # Populate POST request
        self.populate_post_request(self.request)

        # Obtain the response to the POST request
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
        self.populate_invalid_request(self.request)

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
        self.populate_post_request(self.request)

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

# Update view for Translations
class TestUpdateTranslationView(TestCase):
    """
    Translation update view
    """

    url_name="update_translation"
    slug_parameter_name=None # support
    support_model=None # models.Book
    support_model_factory=None
    url_success_slug=None # "details_book"
    support_translation_joint=None # models.TranslationLink
    support_translation_joint_factory=None #factories.TranslationLink
    support_translation_joint_name=None #"book"

    def setUp(self):
        self.factory = RequestFactory()

        # Populate the database with some existing translations
        for _ in range(7):
            translation = factories.TranslationFactory.create()
            if self.slug_parameter_name is not None:
                support_ex = self.support_model_factory.create(user=translation.user)
                kwargs = {self.support_translation_joint_name:support_ex}
                translation_link = self.support_translation_joint_factory.create(item=translation,**kwargs)

        # Select a translation to update
        translation = models.Translation.objects.first()
        
        if self.slug_parameter_name is None:
            kwargs = {}
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))

        self.translations_count = models.Translation.objects.count()
        if self.support_translation_joint is not None:
            self.translations_support_count = self.support_translation_joint.objects.count()

    def test_update_translation_anonymous(self):
        """
        TEST : Update a translation without being logged
        Behavior expected : Redirection to the login page
        """
        
        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))
        self.request.user = AnonymousUser()

        response =  CreateUpdateTranslationView.as_view()(self.request,**kwargs)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_post_update_translation_anonymous(self):
        """
        TEST : Post the translation update form without being logged
        Behavior expected : Redirection to the login page
        """

        # Preparing the request and identify as the user
        self.factory = RequestFactory()

        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.post(reverse(self.url_name,kwargs=kwargs))
        self.request.user = AnonymousUser()

        # Populate POST request
        TestCreateTranslationView.populate_post_request(self.request)

        # Obtain the response to the POST request
        response =  CreateUpdateTranslationView.as_view()(self.request,**kwargs)

        # Assert that no update has been done 
        translation = models.Translation.objects.first()
        self.assertNotEqual(translation.original_word.word,self.request.POST['original_word-word'])

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_get_update_translation_logged_notowner(self):
        """
        TEST : Get the translation update form while being logged
        Behavior expected : The user should not access the page as the user is not the owner
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()

        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))
        self.request.user = user

        response =  CreateUpdateTranslationView.as_view()(self.request,**kwargs)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

    def test_get_update_translation_logged_owner(self):
        """
        TEST : Get the translation update form while being logged
        Behavior expected : The user should access the page as the user is the owner
        """

        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))
        self.request.user = translation.user

        response =  CreateUpdateTranslationView.as_view()(self.request,**kwargs)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)

    def test_post_update_translation_logged_not_owner(self):
        """
        TEST : Post the translation update form while being logged as someone else than the owner of the translation
        Behavior expected : The update should not happen
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()

        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.post(reverse(self.url_name,kwargs=kwargs))
        self.request.user = user

        # Populate POST request
        TestCreateTranslationView.populate_post_request(self.request)

        response =  CreateUpdateTranslationView.as_view()(self.request,**kwargs)

        # Assessing whether the user indeed accesses the page
        translation = models.Translation.objects.get(pk=translation.pk)
        self.assertNotEqual(translation.original_word.word,self.request.POST['original_word-word'])
        self.assertEqual(response.status_code, 403)

    def test_post_update_translation_logged_owner(self):
        """
        TEST : Post the translation update form while being logged as the owner of the translation
        Behavior expected : The update should happen
        """

        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        user = translation.user
        self.request = self.factory.post(reverse(self.url_name,kwargs=kwargs))
        self.request.user = user

        # Populate POST request
        TestCreateTranslationView.populate_post_request(self.request)

        response =  CreateUpdateTranslationView.as_view()(self.request,**kwargs)

        # Assessing whether the user indeed accesses the page
        translation = models.Translation.objects.get(pk=translation.pk)
        self.assertEqual(translation.original_word.word,self.request.POST['original_word-word'])
        self.assertEqual(response.status_code, 302)
        if self.slug_parameter_name is None:
            self.assertEqual(response.url, reverse('list_translations'))
        else:
            kwargs = {self.slug_parameter_name:support.slug}
            self.assertEqual(response.url, reverse(self.url_success_slug,kwargs=kwargs))

    def test_post_update_translation_logged_owner_invalid(self):
        """
        TEST : Post the translation update form while being logged as the owner of the translation with invalid request
        Behavior expected : The update should not happen as the request is invalid
        """

        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        user = translation.user
        self.request = self.factory.post(reverse(self.url_name,kwargs=kwargs))
        self.request.user = user

        # Populate POST request
        TestCreateTranslationView.populate_invalid_request(self.request)

        response =  CreateUpdateTranslationView.as_view()(self.request,**kwargs)

        # Assessing whether the user indeed accesses the page
        translation = models.Translation.objects.get(pk=translation.pk)
        self.assertNotEqual(translation.original_word.word,self.request.POST['original_word-word'])
        self.assertEqual(response.status_code, 200)

class TestUpdateTranslationViewBookSupport(TestUpdateTranslationView):
    """
    Translation update view - Book support
    """

    url_name="update_translation_book"
    slug_parameter_name="slug_book"
    support_model=models.Book
    support_model_factory=factories.BookFactory
    url_success_slug="details_book"
    support_translation_joint=models.TranslationLink
    support_translation_joint_factory=factories.TranslationLinkFactory
    support_translation_joint_name="book"

class TestUpdateTranslationViewDiscussionSupport(TestUpdateTranslationView):
    """
    Translation update view - Discussion support
    """

    url_name="update_translation_discussion"
    slug_parameter_name="slug_discussion"
    support_model=models.Discussion
    support_model_factory=factories.DiscussionFactory
    url_success_slug="details_discussion"
    support_translation_joint=models.TranslationLinkDiscussion
    support_translation_joint_factory=factories.TranslationLinkDiscussionFactory
    support_translation_joint_name="discussion"

class TestUpdateTranslationViewArticleSupport(TestUpdateTranslationView):
    """
    Translation update view - Article support
    """

    url_name="update_translation_article"
    slug_parameter_name="slug_article"
    support_model=models.Article
    support_model_factory=factories.ArticleFactory
    url_success_slug="details_article"
    support_translation_joint=models.TranslationLinkArticle
    support_translation_joint_factory=factories.TranslationLinkArticleFactory
    support_translation_joint_name="article"


class TestListTranslationView(TestSupportList,TestCase):
    """
    List view of one Translation
    """

    factory = RequestFactory()
    url_name = 'list_translations'
    request = factory.get(reverse(url_name))
    supportView = TranslationListView
    supportFactory = factories.TranslationFactory
    
class TestDetailsTranslationView(TestCase):
    """
    Details view of one Translation
    """

    url_name="details_translation"
    slug_parameter_name=None # support
    support_model=None # models.Book
    support_model_factory=None
    url_success_slug=None # "details_book"
    support_translation_joint=None # models.TranslationLink
    support_translation_joint_factory=None #factories.TranslationLink
    support_translation_joint_name=None #"book"

    def setUp(self):
        self.factory = RequestFactory()

        # Populate the database with some existing translations
        for _ in range(7):
            translation = factories.TranslationFactory.create()
            if self.slug_parameter_name is not None:
                support_ex = self.support_model_factory.create(user=translation.user)
                kwargs = {self.support_translation_joint_name:support_ex}
                translation_link = self.support_translation_joint_factory.create(item=translation,**kwargs)

        # Select a translation to update
        translation = models.Translation.objects.first()
        
        if self.slug_parameter_name is None:
            kwargs = {}
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))

        self.translations_count = models.Translation.objects.count()
        if self.support_translation_joint is not None:
            self.translations_support_count = self.support_translation_joint.objects.count()

    def test_details_translation_anonymous(self):
        """
        TEST : Get the details of a translation without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))

        self.request.user = AnonymousUser()
        response =  TranslationView.as_view()(self.request,**kwargs)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_details_translation_logged_not_owner(self):
        """
        TEST : Get the details of a translation not being logged as the owner
        Behavior expected : Forbidden access
        """

        # Executing the page request with a Anonymous User
        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))

        self.request.user = factories.UserFactory.create()
        response =  TranslationView.as_view()(self.request,**kwargs)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 403)

    def test_details_translation_logged_owner(self):
        """
        TEST : Get the details of a translation being logged as the owner
        Behavior expected : Access to the page
        """

        # Executing the page request with a Anonymous User
        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))

        self.request.user = translation.user
        response =  TranslationView.as_view()(self.request,**kwargs)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 200)

class TestDetailsTranslationViewBookSupport(TestDetailsTranslationView):
    """
    Details view of one Translation
    """

    url_name="view_translation_book"
    slug_parameter_name="slug_book"
    support_model=models.Book
    support_model_factory=factories.BookFactory
    support_translation_joint=models.TranslationLink
    support_translation_joint_factory=factories.TranslationLinkFactory
    support_translation_joint_name="book"

class TestDetailsTranslationViewArticleSupport(TestDetailsTranslationView):
    """
    Details view of one Article
    """

    url_name="view_translation_article"
    slug_parameter_name="slug_article"
    support_model=models.Article
    support_model_factory=factories.ArticleFactory
    support_translation_joint=models.TranslationLinkArticle
    support_translation_joint_factory=factories.TranslationLinkArticleFactory
    support_translation_joint_name="article"

class TestDetailsTranslationViewDiscussionSupport(TestDetailsTranslationView):
    """
    Details view of one Discussion
    """

    url_name="view_translation_discussion"
    slug_parameter_name="slug_discussion"
    support_model=models.Discussion
    support_model_factory=factories.DiscussionFactory
    support_translation_joint=models.TranslationLinkDiscussion
    support_translation_joint_factory=factories.TranslationLinkDiscussionFactory
    support_translation_joint_name="discussion"


class TestDeleteTranslationView(TestCase):
    """
    Delete view of one Translation
    """

    url_name="delete_translation"
    slug_parameter_name=None # support
    support_model=None # models.Book
    support_model_factory=None
    url_success_slug=None # "details_book"
    support_translation_joint=None # models.TranslationLink
    support_translation_joint_factory=None #factories.TranslationLink
    support_translation_joint_name=None #"book"

    def setUp(self):
        self.factory = RequestFactory()

        # Populate the database with some existing translations
        for _ in range(7):
            translation = factories.TranslationFactory.create()
            if self.slug_parameter_name is not None:
                support_ex = self.support_model_factory.create(user=translation.user)
                kwargs = {self.support_translation_joint_name:support_ex}
                translation_link = self.support_translation_joint_factory.create(item=translation,**kwargs)

        # Select a translation to update
        translation = models.Translation.objects.first()
        
        if self.slug_parameter_name is None:
            kwargs = {}
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))

        self.translations_count = models.Translation.objects.count()
        if self.support_translation_joint is not None:
            self.translations_support_count = self.support_translation_joint.objects.count()

    def test_delete_translation_anonymous(self):
        """
        TEST : Get the delete view of a translation without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))

        self.request.user = AnonymousUser()
        response =  DeleteTranslationView.as_view()(self.request,**kwargs)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_post_delete_translation_anonymous(self):
        """
        TEST : Post the delete view of a translation without being logged
        Behavior expected : Redirection to the login page
        """

       # Executing the page request with a Anonymous User
        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.post(reverse(self.url_name,kwargs=kwargs))

        self.request.user = AnonymousUser()
        translations_count_before_delete = models.Translation.objects.count()
        response =  DeleteTranslationView.as_view()(self.request,**kwargs)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

        # Checking that the translation has not been deleted
        self.assertEqual(models.Translation.objects.count(), translations_count_before_delete)
        self.assertNotEqual(models.Translation.objects.filter(pk=translation.pk).first(), None)

    def test_delete_translation_logged_owner(self):
        """
        TEST : Get the deletion view of a translation a user is owning while being logged
        Behavior expected : The user should access the translation deletion page
        """

        # Executing the page request with a Anonymous User
        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))

        self.request.user = translation.user
        response =  DeleteTranslationView.as_view()(self.request,**kwargs)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)

    def test_post_delete_translation_logged_owner(self):
        """
        TEST : Post the delete view of a translation a user is owning while being logged
        Behavior expected : Redirection to the login page
        """

       # Executing the page request with a Anonymous User
        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.post(reverse(self.url_name,kwargs=kwargs))

        self.request.user = translation.user
        translations_count_before_delete = models.Translation.objects.count()
        response =  DeleteTranslationView.as_view()(self.request,**kwargs)

        # Assert redirection to the deletion success page
        self.assertEqual(response.status_code, 302)
        if self.slug_parameter_name is None:
            self.assertEqual(response.url, reverse("list_translations"))
        else:
            kwargs = {self.slug_parameter_name:support.slug}
            self.assertEqual(response.url, reverse(self.url_success_slug,kwargs=kwargs))

        # Checking that the translation has not been deleted
        self.assertEqual(models.Translation.objects.count(), translations_count_before_delete-1)
        self.assertEqual(models.Translation.objects.filter(pk=translation.pk).first(), None)

    def test_delete_translation_logged_not_owner(self):
        """
        TEST : Get the deletion view of a translation not being logged as the owner
        Behavior expected : Forbidden access
        """

        # Executing the page request with a Anonymous User
        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))

        self.request.user = factories.UserFactory.create()
        response =  DeleteTranslationView.as_view()(self.request,**kwargs)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

    def test_post_delete_translation_logged_not_owner(self):
        """
        TEST : Post the delete view of a translation while not being logged as the owner
        Behavior expected : Redirection to the login page
        """

       # Executing the page request with a Anonymous User
        if self.slug_parameter_name is None:
            # Select a translation to update
            translation = models.Translation.objects.first()
            kwargs = {}
        else:
            # Select a translation to update
            translation_link = self.support_translation_joint.objects.first()
            translation = translation_link.item
            support = getattr(translation_link,self.support_translation_joint_name)
            kwargs = {self.slug_parameter_name:support.slug}
        kwargs['slug'] = translation.slug
        self.request = self.factory.post(reverse(self.url_name,kwargs=kwargs))

        self.request.user = factories.UserFactory.create()
        translations_count_before_delete = models.Translation.objects.count()
        response =  DeleteTranslationView.as_view()(self.request,**kwargs)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 403)

        # Checking that the translation has not been deleted
        self.assertEqual(models.Translation.objects.count(), translations_count_before_delete)
        self.assertNotEqual(models.Translation.objects.filter(pk=translation.pk).first(), None)

class TestDeleteTranslationViewBookSupport(TestDeleteTranslationView):
    """
    Delete view of one Translation
    """

    url_name="delete_translation_book"
    slug_parameter_name="slug_book"
    support_model=models.Book
    support_model_factory=factories.BookFactory
    url_success_slug="details_book"
    support_translation_joint=models.TranslationLink
    support_translation_joint_factory=factories.TranslationLinkFactory
    support_translation_joint_name="book"

class TestDeleteTranslationViewArticleSupport(TestDeleteTranslationView):
    """
    Delete view of one Translation
    """

    url_name="delete_translation_article"
    url_success_slug="details_article"
    slug_parameter_name="slug_article"
    support_model=models.Article
    support_model_factory=factories.ArticleFactory
    support_translation_joint=models.TranslationLinkArticle
    support_translation_joint_factory=factories.TranslationLinkArticleFactory
    support_translation_joint_name="article"

class TestDeleteTranslationViewDiscussionSupport(TestDeleteTranslationView):
    """
    Delete view of one Translation
    """

    url_name="delete_translation_discussion"
    url_success_slug="details_discussion"
    slug_parameter_name="slug_discussion"
    support_model=models.Discussion
    support_model_factory=factories.DiscussionFactory
    support_translation_joint=models.TranslationLinkDiscussion
    support_translation_joint_factory=factories.TranslationLinkDiscussionFactory
    support_translation_joint_name="discussion"