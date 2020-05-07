from django.test import RequestFactory, TestCase
from .factories import UserFactoryEmpty
from django.contrib.auth.models import AnonymousUser
from .views import *

class TestHomeNoMember(TestCase):
    def test_home_nomember(self):
        resp = self.client.get('/public/')
        self.assertEqual(resp.status_code, 200)

class TestRootNoMember(TestCase):
    def test_root_nomember(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 301)

class TestBooksList(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user_empty = UserFactoryEmpty.create()

    def test_books_list(self):
        request = self.factory.get('/public/member/books/list')
        request.user = AnonymousUser()
        response = BooksListView.as_view()(request)

        # Checking whether the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_books_list_logged_empty(self):
        request = self.factory.get('/public/member/books/list')
        request.user = self.user_empty
        response = BooksListView.as_view()(request)
        
        # Checking whether the user with no activity does not really see any book
        self.assertContains(response,'No lectures yet')
        self.assertEqual(len(response.context_data['object_list']),0)
        self.assertEqual(response.status_code, 200)
