from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
from .views import *
from . import models
from django.urls import reverse
import factory
from . import factories
from .tests_commons import *

class TestHomeNoMember(TestCase):
    def test_home_nomember(self):
        resp = self.client.get('/public/')
        self.assertEqual(resp.status_code, 200)

class TestRootNoMember(TestCase):
    def test_root_nomember(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 301)

class TestArticlesList(TestSupportList,TestCase):

    factory = RequestFactory()
    url_name = 'list_article'
    request = factory.get(reverse(url_name))
    supportView = ArticlesListView
    supportFactory = factories.ArticleFactory

class TestDiscussionsList(TestSupportList,TestCase):

    factory = RequestFactory()
    url_name = 'list_discussion'
    request = factory.get(reverse(url_name))
    supportView = DiscussionsListView
    supportFactory = factories.DiscussionFactory

class TranslationsList(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get(reverse('list_translations'))
        if hasattr(TranslationListView,'paginate_by'):
            self.paginate_by = TranslationListView.paginate_by
        else:
            self.paginate_by = False

    def test_translations_list_anonymous(self):
        self.request.user = AnonymousUser()
        response = TranslationListView.as_view()(self.request)

        # Checking whether the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_translations_list_logged_empty(self):

        # User not linked with any book
        user_empty = factories.UserFactory.create()

        self.request.user = user_empty
        response = TranslationListView.as_view()(self.request)
        
        # Checking whether the user with no activity does not really see any translation
        self.assertEqual(len(response.context_data['object_list']),0)
        self.assertEqual(response.status_code, 200)

    def test_translations_list_logged_not_empty(self):

        # User linked with translations
        user_notempty_1 = factories.UserFactory.create()
        user_notempty_2 = factories.UserFactory.create()
        if self.paginate_by:
            nb_translations_1 = random.randint(1,self.paginate_by)
        else:
            nb_translations_1 = random.randint(1,100)
        nb_translations_2 = random.randint(1,100)
        for _ in range(nb_translations_1):
            factories.TranslationFactory.create(user=user_notempty_1)
        for _ in range(nb_translations_2):
            factories.TranslationFactory.create(user=user_notempty_2)

        self.request.user = user_notempty_1
        response = TranslationListView.as_view()(self.request)

        # Checking whether the user is displayed with all his translations
        self.assertEqual(len(response.context_data['object_list']),nb_translations_1)
        self.assertEqual(response.status_code, 200)

    def test_translations_with_pagination(self):
        if self.paginate_by:
            # User linked with translations
            user_notempty_1 = factories.UserFactory.create()
            user_notempty_2 = factories.UserFactory.create()
            nb_translations_1 = random.randint(self.paginate_by+1,100)
            nb_translations_2 = random.randint(1,100)
            for _ in range(nb_translations_1):
                factories.TranslationFactory.create(user=user_notempty_1)
            for _ in range(nb_translations_2):
                factories.TranslationFactory.create(user=user_notempty_2)

            for i in range(1,int(nb_translations_1/self.paginate_by)+1):
                self.request = self.factory.get(reverse('list_translations'))
                self.request.GET = self.request.GET.copy()
                self.request.GET['page'] = i
                self.request.user = user_notempty_1
                response = TranslationListView.as_view()(self.request)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(len(response.context_data['object_list']) == self.paginate_by)
            
            remaining = nb_translations_1 % self.paginate_by
            if remaining!=0:
                self.request = self.factory.get(reverse('list_translations'))
                self.request.user = user_notempty_1
                self.request.GET = self.request.GET.copy()
                self.request.GET['page']=int(nb_translations_1/self.paginate_by)+1
                response = TranslationListView.as_view()(self.request)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(len(response.context_data['object_list']) == remaining)

        else:
            pass