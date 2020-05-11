from django.test import RequestFactory, TestCase
from .factories import UserFactory, BookFactory
from django.contrib.auth.models import AnonymousUser
from .views import *
from . import models

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

    def test_books_list_anonymous(self):
        request = self.factory.get('/public/member/books/list')
        request.user = AnonymousUser()
        response = BooksListView.as_view()(request)

        # Checking whether the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_books_list_logged_empty(self):

        # User not linked with any book
        user_empty = UserFactory.create()

        request = self.factory.get('/public/member/books/list')
        request.user = user_empty
        response = BooksListView.as_view()(request)
        
        # Checking whether the user with no activity does not really see any book
        self.assertContains(response,'No lectures yet')
        self.assertEqual(len(response.context_data['object_list']),0)
        self.assertEqual(response.status_code, 200)

    def test_books_list_logged_not_empty(self):

        # User linked with books
        user_notempty_1 = UserFactory.create()
        user_notempty_2 = UserFactory.create()
        nb_books_1 = 8
        nb_books_2 = 4
        for i in range(nb_books_1):
            BookFactory.create(user=user_notempty_1)
        for i in range(nb_books_2):
            BookFactory.create(user=user_notempty_2)

        request = self.factory.get('/public/member/books/list')
        request.user = user_notempty_1
        response = BooksListView.as_view()(request)

        # Checking whether the user is displayed with all his books
        self.assertEqual(len(response.context_data['object_list']),nb_books_1)
        self.assertEqual(response.status_code, 200)

