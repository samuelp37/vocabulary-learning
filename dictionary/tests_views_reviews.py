from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
from .views import *
from . import models
from django.urls import reverse
import factory
from . import factories
from .tests_commons import *
import datetime

# Creation view for Review
class TestCreateReviewView(TestCase):
    """
    Review creation view
    """

    url_name="add_review"
    slug_parameter_name=None
    support_model=None # models.Book
    support_model_factory=None

    def setUp(self):

        self.factory = RequestFactory()
        if self.slug_parameter_name is None:
            self.request = self.factory.get(reverse(self.url_name))
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
            self.request = self.factory.get(reverse(self.url_name,kwargs=kwargs))

        # Populate the database with existing review
        for _ in range(7):
            quizz = factories.QuizzFactory.create()
            quizz_link = factories.QuizzLinkItemFactory.create(quizz=quizz)

        self.reviews_count = models.Quizz.objects.count()

    def test_create_review_anonymous(self):
        """
        TEST : Get the review creation form without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        self.request.user = AnonymousUser()
        if self.slug_parameter_name is None:
            response = CreateReviewView.as_view()(self.request)
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
            response =  CreateReviewView.as_view()(self.request,**kwargs)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_post_create_review_anonymous(self):
        """
        TEST : Post the review creation form without being logged
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

        # Creatng a POST request
        self.request.POST = self.request.POST.copy()
        self.request.POST['number_questions'] = 10
        self.request.POST['original_to_translated'] = True
        self.request.POST['ordering_policy'] = "random"

        # Obtain the response to the POST request
        response =  CreateReviewView.as_view()(self.request,**kwargs)

        # Assert no review has been created
        self.assertEqual(models.Quizz.objects.count(),self.reviews_count)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)     

    def test_get_create_review_logged(self):
        """
        TEST : Get the review creation form while being logged
        Behavior expected : The user should access the translation creation page
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        self.request.user = user

        # Executing a HTTP request towards the page
        if self.slug_parameter_name is None:
            response = CreateReviewView.as_view()(self.request)
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
            response =  CreateReviewView.as_view()(self.request,**kwargs)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)

    def test_post_create_review_logged_case1(self):
        """
        TEST : Post the review creation form while being logged
        Behavior expected : Review created
        """

        #########
        # Testing 2 cases / Requested number of trasnlations below the total number for the user
        #########

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        if self.slug_parameter_name is None:
            self.request = self.factory.post(reverse(self.url_name))
            kwargs = {}
        else:
            support_ex = self.support_model_factory.create()
            kwargs = {self.slug_parameter_name:support_ex.slug}
            self.request = self.factory.post(reverse(self.url_name,kwargs=kwargs))

        nb_questions = 10
        nb_translations = 20

        # Create a user and Populate the database with existing trasnlation from this user
        self.request.user = factories.UserFactory.create()
        for _ in range(nb_translations):
            translation = factories.TranslationFactory.create(user=self.request.user)

        # Creatng a POST request
        self.request.POST = self.request.POST.copy()
        self.request.POST['number_questions'] = nb_questions
        self.request.POST['original_to_translated'] = True
        self.request.POST['ordering_policy'] = "random"

        # Obtain the response to the POST request
        response =  CreateReviewView.as_view()(self.request,**kwargs)

        # Assert a review has been created and the correct number of items too
        self.assertEqual(models.Quizz.objects.count(),self.reviews_count+1)
        quizz = models.Quizz.objects.last()
        self.assertEqual(models.QuizzLinkItem.objects.filter(quizz=quizz).count(),min([nb_questions,nb_translations]))
        quizz_link_item = models.QuizzLinkItem.objects.last()
        quizz_item = quizz_link_item.quizz_item

        # Preparing arguments 
        kwargs_redirection = {'slug_item':quizz_item.slug,'slug_review':quizz.slug}

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('quizz_review_item',kwargs=kwargs_redirection))
        
    def test_post_create_review_logged_case2(self):
        """
        TEST : Post the review creation form while being logged
        Behavior expected : Review created
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

        nb_questions = 11
        nb_translations = 10

        # Create a user and Populate the database with existing trasnlation from this user
        self.request.user = factories.UserFactory.create()
        for _ in range(nb_translations):
            translation = factories.TranslationFactory.create(user=self.request.user)

        # Creatng a POST request
        self.request.POST = self.request.POST.copy()
        self.request.POST['number_questions'] = nb_questions
        self.request.POST['original_to_translated'] = False
        self.request.POST['ordering_policy'] = "random"

        # Obtain the response to the POST request
        response =  CreateReviewView.as_view()(self.request,**kwargs)

        # Assert a review has been created and the correct number of items too
        self.assertEqual(models.Quizz.objects.count(),self.reviews_count+1)
        quizz = models.Quizz.objects.latest('pk')
        self.assertEqual(models.QuizzLinkItem.objects.filter(quizz=quizz).count(),min([nb_questions,nb_translations]))
        
    def test_post_create_review_logged_negative_questions(self):
        """
        TEST : Post the review creation form while being logged
        Behavior expected : Review created
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

        nb_questions = -1
        default_nb_questions = 10
        nb_translations = 10

        # Create a user and Populate the database with existing trasnlation from this user
        self.request.user = factories.UserFactory.create()
        for _ in range(nb_translations):
            translation = factories.TranslationFactory.create(user=self.request.user)

        # Creatng a POST request
        self.request.POST = self.request.POST.copy()
        self.request.POST['number_questions'] = nb_questions
        self.request.POST['original_to_translated'] = True
        self.request.POST['ordering_policy'] = "random"

        # Obtain the response to the POST request
        response =  CreateReviewView.as_view()(self.request,**kwargs)

        # Assert a review has been created and the correct number of items too
        self.assertEqual(models.Quizz.objects.count(),self.reviews_count+1)
        quizz = models.Quizz.objects.latest('pk')
        self.assertEqual(models.QuizzLinkItem.objects.filter(quizz=quizz).count(),min([default_nb_questions,nb_translations]))
        
class TestListReviewView(TestSupportList,TestCase):
    """
    List view of one Review
    """

    factory = RequestFactory()
    url_name = 'list_reviews'
    request = factory.get(reverse(url_name))
    supportView = ReviewsListView
    supportFactory = factories.QuizzFactory

# Details view for Review
class TestDetailsReviewView(TestCase):
    """
    Review details view
    """

    url_name="details_review"
    slug_parameter_name=None
    support_model=None # models.Book
    support_model_factory=None

    def setUp(self):

        self.factory = RequestFactory()

    def test_details_review_anonymous(self):
        """
        TEST : Get the details review view without being logged
        Behavior expected : Redirection to the login page
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug}))

        # Executing the page request with a Anonymous User
        self.request.user = AnonymousUser()
        response =  ReviewView.as_view()(self.request,slug_review=review.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_get_create_review_logged_not_owner(self):
        """
        TEST : Get the review view not being logged as the owner of the review
        Behavior expected : Forbidden access
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug}))

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        self.request.user = user

        # Executing a HTTP request towards the page
        response =  ReviewView.as_view()(self.request,slug_review=review.slug)

        # Assessing forbidden access
        self.assertEqual(response.status_code, 403)

    def test_get_create_review_logged_owner(self):
        """
        TEST : Get the details of the review the user is owning
        Behavior expected : Page accessible
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug}))

        # Simulate a user and perform a request
        self.request.user = review.user

        # Executing a HTTP request towards the page
        response =  ReviewView.as_view()(self.request,slug_review=review.slug)

        # Assessing forbidden access
        self.assertEqual(response.status_code, 200)

# Resume view for Review
class TestResumeReviewView(TestCase):
    """
    Review Resume view
    """

    url_name="resume_review"
    slug_parameter_name=None
    support_model=None # models.Book
    support_model_factory=None

    def setUp(self):

        self.factory = RequestFactory()

    def test_resume_review_anonymous(self):
        """
        TEST : Get the resume review view without being logged
        Behavior expected : Redirection to the login page
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        nb_questions = 20
        for _ in range(nb_questions):
            quizz_link = factories.QuizzLinkItemFactory.create(quizz=review)
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug}))

        # Executing the page request with a Anonymous User
        self.request.user = AnonymousUser()
        response =  ResumeReviewView.as_view()(self.request,slug_review=review.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_get_resume_review_logged_not_owner(self):
        """
        TEST : Get the resume review view not being logged as the owner of the review
        Behavior expected : Forbidden access
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        nb_questions = 20
        for _ in range(nb_questions):
            quizz_link = factories.QuizzLinkItemFactory.create(quizz=review)
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug}))

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        self.request.user = user

        # Executing a HTTP request towards the page
        response =  ResumeReviewView.as_view()(self.request,slug_review=review.slug)

        # Assessing forbidden access
        self.assertEqual(response.status_code, 403)

    def test_get_create_review_logged_owner(self):
        """
        TEST : Get the resume view of the review the user is owning with still some questions not answered
        Behavior expected : Redirection towards a question
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        nb_questions = 20
        for _ in range(nb_questions):
            quizz_item = factories.QuizzItemFactory(success=None)
            quizz_link = factories.QuizzLinkItemFactory.create(quizz=review,quizz_item=quizz_item)
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug}))

        # Simulate a user and perform a request
        self.request.user = review.user

        # Executing a HTTP request towards the page
        response =  ResumeReviewView.as_view()(self.request,slug_review=review.slug)

        quizz_link_item = models.QuizzLinkItem.objects.filter(quizz=review).first()
        quizz_item = quizz_link_item.quizz_item

        # Preparing arguments 
        kwargs_redirection = {'slug_item':quizz_item.slug,'slug_review':review.slug}

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('quizz_review_item',kwargs=kwargs_redirection))

    def test_get_create_review_logged_owner_no_remaining(self):
        """
        TEST : Get the resume view of the review the user is owning with all questions answered
        Behavior expected : Redirection towards the detail page of the review
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        nb_questions = 20
        for _ in range(nb_questions):
            quizz_item = factories.QuizzItemFactory() # success will be assigned True/False
            quizz_link = factories.QuizzLinkItemFactory.create(quizz=review,quizz_item=quizz_item)
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug}))

        # Simulate a user and perform a request
        self.request.user = review.user

        # Executing a HTTP request towards the page
        response =  ResumeReviewView.as_view()(self.request,slug_review=review.slug)

        # Preparing arguments 
        kwargs_redirection = {'slug_review':review.slug}

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('details_review',kwargs=kwargs_redirection))


# Quizz Review/Item view
class TestQuizzReviewItemView(TestCase):
    """
    Quizz Review Item view
    """

    url_name="quizz_review_item"
    slug_parameter_name=None
    support_model=None # models.Book
    support_model_factory=None

    def setUp(self):

        self.factory = RequestFactory()

    def test_review_item_view_anonymous(self):
        """
        TEST : Get the review item view without being logged
        Behavior expected : Redirection to the login page
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        nb_questions = 20
        for _ in range(nb_questions):
            quizz_link = factories.QuizzLinkItemFactory.create(quizz=review)
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug,'slug_item':quizz_link.quizz_item.slug}))

        # Executing the page request with a Anonymous User
        self.request.user = AnonymousUser()
        response =  QuizzReviewItemView.as_view()(self.request,slug_review=review.slug,slug_item=quizz_link.quizz_item.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_get_review_item_view_logged_not_owner(self):
        """
        TEST : Get the review item view not being logged as the owner of the review
        Behavior expected : Forbidden access
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        nb_questions = 20
        for _ in range(nb_questions):
            quizz_link = factories.QuizzLinkItemFactory.create(quizz=review)
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug,'slug_item':quizz_link.quizz_item.slug}))

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        self.request.user = user

        # Executing a HTTP request towards the page
        response =  QuizzReviewItemView.as_view()(self.request,slug_review=review.slug,slug_item=quizz_link.quizz_item.slug)

        # Assessing forbidden access
        self.assertEqual(response.status_code, 403)

    def test_get_review_item_view_logged_owner(self):
        """
        TEST : Get the review item view
        Behavior expected : The page should be displayed normally
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        nb_questions = 20
        for _ in range(nb_questions):
            quizz_item = factories.QuizzItemFactory(success=None)
            quizz_link = factories.QuizzLinkItemFactory.create(quizz=review,quizz_item=quizz_item)
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug,'slug_item':quizz_link.quizz_item.slug}))

        # Simulate a user and perform a request
        self.request.user = review.user

        # Executing a HTTP request towards the page
        response =  QuizzReviewItemView.as_view()(self.request,slug_review=review.slug,slug_item=quizz_link.quizz_item.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 200)

# Quizz Analysis Review/Item view
class TestQuizzAnalysisReviewItemView(TestCase):
    """
    Quizz Analysis Review Item view
    """

    url_name="quizz_analysis_review_item"
    slug_parameter_name=None
    support_model=None # models.Book
    support_model_factory=None

    def setUp(self):

        self.factory = RequestFactory()

    def test_analysis_review_item_view_anonymous(self):
        """
        TEST : Get the analysis review item view without being logged
        Behavior expected : Redirection to the login page
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        nb_questions = 20
        for _ in range(nb_questions):
            quizz_link = factories.QuizzLinkItemFactory.create(quizz=review)
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug,'slug_item':quizz_link.quizz_item.slug,'success':1}))

        # Executing the page request with a Anonymous User
        self.request.user = AnonymousUser()
        response =  QuizzAnalysisReviewItemView.as_view()(self.request,slug_review=review.slug,slug_item=quizz_link.quizz_item.slug, success=1)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_get_analysis_review_item_view_logged_not_owner(self):
        """
        TEST : Get the analysis review item view not being logged as the owner of the review
        Behavior expected : Forbidden access
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        nb_questions = 20
        for _ in range(nb_questions):
            quizz_link = factories.QuizzLinkItemFactory.create(quizz=review)
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug,'slug_item':quizz_link.quizz_item.slug,'success':1}))

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        self.request.user = user

        # Executing a HTTP request towards the page
        response =  QuizzAnalysisReviewItemView.as_view()(self.request,slug_review=review.slug,slug_item=quizz_link.quizz_item.slug,success=1)

        # Assessing forbidden access
        self.assertEqual(response.status_code, 403)

    def test_get_analysis_review_item_view_logged_owner_remaining(self):
        """
        TEST : Get the analysis review item view
        Behavior expected : The request should be processed and the user redirected to the next question
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        nb_questions = 20
        for _ in range(nb_questions):
            quizz_item = factories.QuizzItemFactory(success=None)
            quizz_link = factories.QuizzLinkItemFactory.create(quizz=review,quizz_item=quizz_item)
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug,'slug_item':quizz_link.quizz_item.slug,'success':1}))

        # Simulate a user and perform a request
        self.request.user = review.user

        # Executing a HTTP request towards the page
        response =  QuizzAnalysisReviewItemView.as_view()(self.request,slug_review=review.slug,slug_item=quizz_link.quizz_item.slug,success=1)

        # Assert modification of the success attribute
        review_link_item = models.QuizzLinkItem.objects.get(pk=quizz_link.quizz_item.pk)
        self.assertEqual(review_link_item.quizz_item.success,True)

        # Assert redirection to the next question
        next_quizz_item = review.items.all().filter(success=None).first()
        kwargs_redirection = {'slug_review':review.slug,'slug_item':next_quizz_item.slug}
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('quizz_review_item',kwargs=kwargs_redirection))

    def test_get_analysis_review_item_view_logged_owner_no_remaining(self):
        """
        TEST : Get the analysis review item view with no remaining question itm available
        Behavior expected : The request should be processed and the user redirected to the details of the review
        """

        # Creating a review
        review = factories.QuizzFactory.create()
        nb_questions = 20
        for _ in range(nb_questions-1):
            quizz_item = factories.QuizzItemFactory(success=True)
            quizz_link = factories.QuizzLinkItemFactory.create(quizz=review,quizz_item=quizz_item)
        quizz_item = factories.QuizzItemFactory(success=None)
        quizz_link = factories.QuizzLinkItemFactory.create(quizz=review,quizz_item=quizz_item)
        self.request = self.factory.get(reverse(self.url_name,kwargs={'slug_review':review.slug,'slug_item':quizz_link.quizz_item.slug,'success':0}))

        # Simulate a user and perform a request
        self.request.user = review.user

        # Executing a HTTP request towards the page
        response =  QuizzAnalysisReviewItemView.as_view()(self.request,slug_review=review.slug,slug_item=quizz_link.quizz_item.slug,success=0)

        # Assert modification of the success attribute
        review_link_item = models.QuizzLinkItem.objects.get(pk=quizz_link.quizz_item.pk)
        self.assertEqual(review_link_item.quizz_item.success,False)

        # Assert redirection to the next question
        kwargs_redirection = {'slug_review':review.slug}
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('details_review',kwargs=kwargs_redirection))

class TestDeleteReviewView(TestCase):
    """
    Delete view of one Review
    """

    def setUp(self):
        self.factory = RequestFactory()

        # Populate the database with some existing books
        for _ in range(7):
            factories.QuizzFactory.create()

        self.reviews_count = models.Quizz.objects.count()

    def test_delete_review_anonymous(self):
        """
        TEST : Get the delete view of a review without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        quizz = models.Quizz.objects.first()
        self.request = self.factory.get(reverse('delete_review',kwargs={'slug_review':quizz.slug}))
        
        self.request.user = AnonymousUser()
        response = DeleteReviewView.as_view()(self.request,slug_review=quizz.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)
    
    def test_post_delete_review_anonymous(self):
        """
        TEST : Post the delete view of a review without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        quizz = models.Quizz.objects.first()
        self.request = self.factory.post(reverse('delete_review',kwargs={'slug_review':quizz.slug}))
        
        self.request.user = AnonymousUser()
        reviews_count_before_delete = models.Quizz.objects.count()
        response = DeleteReviewView.as_view()(self.request,slug_review=quizz.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

        # Checking that the book has not been deleted
        self.assertEqual(models.Quizz.objects.count(), reviews_count_before_delete)
        self.assertNotEqual(models.Quizz.objects.filter(pk=quizz.pk).first(), None)

    def test_delete_review_logged_owner(self):
        """
        TEST : Get the deletion view of a review a user is owning while being logged
        Behavior expected : The user should access the review deletion page
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        quizz = factories.QuizzFactory.create(user=user)
        self.request = self.factory.get(reverse('delete_review',kwargs={'slug_review':quizz.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = DeleteReviewView.as_view()(self.request,slug_review=quizz.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)

    def test_post_delete_review_logged_owner(self):
        """
        TEST : Post the deletion view of a review a user is owning while being logged
        Behavior expected : The user should access the review deletion page
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        quizz = factories.QuizzFactory.create(user=user)
        self.request = self.factory.post(reverse('delete_review',kwargs={'slug_review':quizz.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        reviews_count_before_delete = models.Quizz.objects.count()
        response = DeleteReviewView.as_view()(self.request,slug_review=quizz.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_reviews'))

        # Checking whether the book has been deleted
        self.assertEqual(models.Quizz.objects.count(), reviews_count_before_delete-1)
        self.assertEqual(models.Quizz.objects.filter(pk=quizz.pk).first(), None)

    def test_delete_review_logged_not_owner(self):
        """
        TEST : Get the deletion view of a review a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        quizz = factories.QuizzFactory.create()
        self.request = self.factory.get(reverse('delete_review',kwargs={'slug_review':quizz.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = DeleteReviewView.as_view()(self.request,slug_review=quizz.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

    def test_post_delete_review_logged_not_owner(self):
        """
        TEST : Post the deletion view of a review a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        quizz = factories.QuizzFactory.create()
        self.request = self.factory.post(reverse('delete_review',kwargs={'slug_review':quizz.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        reviews_count_before_delete = models.Quizz.objects.count()
        response = DeleteReviewView.as_view()(self.request,slug_review=quizz.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

        # Checking that the book has not been deleted
        self.assertEqual(models.Quizz.objects.count(), reviews_count_before_delete)
        self.assertNotEqual(models.Quizz.objects.filter(pk=quizz.pk).first(), None)