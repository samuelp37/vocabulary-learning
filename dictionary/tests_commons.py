from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
from .views import *
from . import models
from django.urls import reverse
import factory
from . import factories

class TestSupportList(object):
    """
    Class grouping test for models inheriting from Support abstract class (The criteria of validity are nearly similar for these)
    """
    # This test works as an abstract class. Therefore a special architecture is used there.
    # The following variables need to be specified in order for the test to work.
    # factory = None
    # url_name = None
    # request = factory.get(reverse(url_name))
    # supportView = None
    # supportFactory = None

    def setUp(self):
        # Testing whether the pagination is enabled for the view
        if hasattr(self.supportView,'paginate_by'):
            self.paginate_by = self.supportView.paginate_by
        else:
            self.paginate_by = False

    def test_support_list_anonymous(self):
        """
        TEST : Get the list of the books without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        self.request.user = AnonymousUser()
        response = self.supportView.as_view()(self.request)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_support_list_logged(self):
        """
        TEST : Get the list of the books while being logged. As a simplified case, we first test in the case where the number of books can fit in one page (even with pagination).
        Behavior expected : The user should access the list of his books (only his)
        """

        # Creating 2 users each one having a certain number of books
        user_notempty_1 = factories.UserFactory.create()
        user_notempty_2 = factories.UserFactory.create()
        if self.paginate_by:
            nb_support_1 = random.randint(1,self.paginate_by-1)
            nb_support_2 = random.randint(1,self.paginate_by-1)
        else:
            nb_support_1 = random.randint(1,9)
            nb_support_2 = random.randint(1,9)
        for _ in range(nb_support_1):
            self.supportFactory.create(user=user_notempty_1)
        for _ in range(nb_support_2):
            self.supportFactory.create(user=user_notempty_2)

        # Executing the equest against the view
        self.request.user = user_notempty_1
        response = self.supportView.as_view()(self.request)

        # Checking whether the page is indeed accessed and the number of books diplayed correspond to the number of book of the users
        self.assertEqual(len(response.context_data['object_list']),nb_support_1)
        self.assertEqual(response.status_code, 200)

    def test_support_list_with_pagination(self):
        """
        TEST : Testing whether the number of books displayed for a user is valid, even with pagination
        Behavior expected : the number of books displayed should be valid and the user should have access
        """

        # Limiting the test to the pagination case
        if self.paginate_by:

            # Creating 2 users. The user used for the test should have a minimum amount of book for the test (pagination+1)
            user_notempty_1 = factories.UserFactory.create()
            user_notempty_2 = factories.UserFactory.create()
            nb_supports_1 = random.randint(self.paginate_by+1,100)
            nb_supports_2 = random.randint(1,100)
            for _ in range(nb_supports_1):
                self.supportFactory.create(user=user_notempty_1)
            for _ in range(nb_supports_2):
                self.supportFactory.create(user=user_notempty_2)

            # Testing whether each page is isplaying the correct number of books
            for i in range(1,int(nb_supports_1/self.paginate_by)+1):

                # Preparing the GET request and executing
                self.request = self.factory.get(reverse(self.url_name))
                self.request.GET = self.request.GET.copy()
                self.request.GET['page'] = i
                self.request.user = user_notempty_1
                response = self.supportView.as_view()(self.request)

                # Checking whether the number of books displayed is correct and the page is indeed accessed
                self.assertEqual(response.status_code, 200)
                self.assertTrue(len(response.context_data['object_list']) == self.paginate_by)
            
            # Getting the remaining books (last, not full page)
            remaining = nb_supports_1 % self.paginate_by
            if remaining!=0:

                # Preparing the GET request and executing it
                self.request = self.factory.get(reverse(self.url_name))
                self.request.user = user_notempty_1
                self.request.GET = self.request.GET.copy()
                self.request.GET['page']=int(nb_supports_1/self.paginate_by)+1
                response = self.supportView.as_view()(self.request)

                # Asserting whether the user can access the page and the displayed number of books is correct
                self.assertEqual(response.status_code, 200)
                self.assertTrue(len(response.context_data['object_list']) == remaining)