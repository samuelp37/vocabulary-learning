from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
from .views import *
from . import models
from django.urls import reverse
import factory
from . import factories
from .tests_commons import *

class TestCreateDiscussionView(TestCase):
    """
    Discussion creation view
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get(reverse('add_discussion'))

        # Populate the database with some existing books
        for _ in range(7):
            factories.DiscussionFactory.create()

        self.topics_count = models.Topic.objects.count()
        self.discussions_count = models.Discussion.objects.count()

    def test_create_discussion_anonymous(self):
        """
        TEST : Get the discussion creation form without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        self.request.user = AnonymousUser()
        response = CreateUpdateDiscussionView.as_view()(self.request)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_post_create_discussion_anonymous(self):
        """
        TEST : Post the discussion creation form without being logged
        Behavior expected : Redirection to the login page
        """

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_discussion'))
        self.request.user = AnonymousUser()

        # Creatng a POST request with valid parameters
        self.request.POST = self.request.POST.copy()
        self.request.POST['topic-name'] = factory.Faker('word')
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        response = CreateUpdateDiscussionView.as_view()(self.request)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_get_create_discussion_logged(self):
        """
        TEST : Get the discussion creation form while being logged
        Behavior expected : The user should access the discussion creation page
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        self.request.user = user

        # Executing a HTTP request towards the page
        response = CreateUpdateDiscussionView.as_view()(self.request)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)

    def test_post_create_discussion_logged_notopic(self):
        """
        TEST : Executing a POST request to create a discussion while omitting to specify topic's information
        Behavior expected : No discussion neither topic should be created and the user should be redirected back to the discussion creation form.
        """

        # Create a fake user
        user = factories.UserFactory.create()

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_discussion'))
        self.request.user = user

        # Creatng a POST request while omitting the author first name
        self.request.POST = self.request.POST.copy()
        self.request.POST['topic-name'] = ''
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        # Executing the request
        response = CreateUpdateDiscussionView.as_view()(self.request)

        # Checking whether no discussion neither topic has been created
        self.assertEqual(models.Discussion.objects.count(),self.discussions_count)
        self.assertEqual(models.Topic.objects.count(),self.topics_count)

        # Checking whether the page is unchanged and the user is reaching again the book creation form
        self.assertEqual(response.status_code, 200)

    def test_post_create_discussion_logged_notitle(self):
        """
        TEST : Executing a POST request to create a discussion while omitting to specify the title
        Behavior expected : No discussion should be created and the user should be redirected back to the book creation form.
        """

        # Create a fake user
        user = factories.UserFactory.create()

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_discussion'))
        self.request.user = user

        # Creatng a POST request while omitting the title
        self.request.POST = self.request.POST.copy()
        self.request.POST['topic-name'] = factory.Faker('word')
        self.request.POST['title'] = ''
        self.request.POST['language'] = factories.LanguageFactory.create().pk
        
        # Executing the request
        response = CreateUpdateDiscussionView.as_view()(self.request)

        # Checking whether no discussion has been created
        self.assertEqual(models.Discussion.objects.count(),self.discussions_count)

        # Checking whether the page is unchanged and the user is reaching again the book creation form
        self.assertEqual(response.status_code, 200)

    def test_post_create_discussion_logged_valid_not_existing_topic(self):
        """
        TEST : Executing a POST request to create a discussion (valid request) and the topic is not on the database
        Behavior expected : A discussion and a topic should be created
        """
        
        # Create a fake user
        user = factories.UserFactory.create()

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_discussion'))
        self.request.user = user

        # Creatng a POST request with valid parameters
        self.request.POST = self.request.POST.copy()
        self.request.POST['topic-name'] = factory.Faker('word').generate({})[:70]
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        # Executing the request
        response = CreateUpdateDiscussionView.as_view()(self.request)

        # Assessing that both a discussion and a topic have been created
        self.assertEqual(models.Topic.objects.count(),self.topics_count+1)
        self.assertEqual(models.Discussion.objects.count(),self.discussions_count+1)

        # Assessing that te user is redirected to the list of books
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_discussion'))

    def test_post_create_discussion_logged_valid_existing_topic(self):
        """
        TEST : Executing a POST request to create a discussion (valid request) and the topic are already on the database
        Behavior expected : A discussion should be created but no topic should be created (just a reference to it)
        """
        
        user = factories.UserFactory.create()

        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_discussion'))
        self.request.user = user
        self.request.POST = self.request.POST.copy()

        topic = models.Topic.objects.first()
        self.request.POST['topic-name'] = topic.name
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk
        response = CreateUpdateDiscussionView.as_view()(self.request)

        # Checking whether a discussion is created but no topic
        self.assertEqual(models.Topic.objects.count(),self.topics_count)
        self.assertEqual(models.Discussion.objects.count(),self.discussions_count+1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_discussion'))

class TestUpdateDiscussionView(TestCase):
    """
    Discussion update view
    """

    def setUp(self):
        self.factory = RequestFactory()

        # Populate the database with some existing books
        for _ in range(7):
            factories.DiscussionFactory.create()

        self.topics_count = models.Topic.objects.count()
        self.discussions_count = models.Discussion.objects.count()

    def test_update_discussion_anonymous(self):
        """
        TEST : Update a discussion without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        discussion = models.Discussion.objects.first()
        self.request = self.factory.get(reverse('update_discussion',kwargs={'slug_discussion':discussion.slug}))
        
        self.request.user = AnonymousUser()
        response = CreateUpdateDiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_post_update_discussion_anonymous(self):
        """
        TEST : Update a discussion without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        discussion = models.Discussion.objects.first()
        self.request = self.factory.post(reverse('update_discussion',kwargs={'slug_discussion':discussion.slug}))
        
        # Configuring the POST request with valid parameters
        self.request.POST = self.request.POST.copy()
        self.request.POST['topic-name'] = factory.Faker('word').generate({})[:70]
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        self.request.user = AnonymousUser()
        response = CreateUpdateDiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_update_discussion_logged_owner(self):
        """
        TEST : Update a discussion a user is owning while being logged
        Behavior expected : The user should access the discussion update form
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        discussion = factories.DiscussionFactory.create(user=user)
        self.request = self.factory.get(reverse('update_discussion',kwargs={'slug_discussion':discussion.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = CreateUpdateDiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)
    
    def test_update_discussion_logged_not_owner(self):
        """
        TEST : Update a discussion a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        discussion = models.Discussion.objects.first()
        self.request = self.factory.get(reverse('update_discussion',kwargs={'slug_discussion':discussion.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = CreateUpdateDiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

    def test_post_update_discussion_logged_not_owner(self):
        """
        TEST : Update a discussion a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        discussion = models.Discussion.objects.first()
        self.request = self.factory.post(reverse('update_discussion',kwargs={'slug_discussion':discussion.slug}))
        self.request.user = user

         # Configuring the POST request with valid parameters
        self.request.POST = self.request.POST.copy()
        self.request.POST['topic-name'] = factory.Faker('word').generate({})[:70]
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        # Executing a HTTP request towards the page
        response = CreateUpdateDiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

    def test_post_update_discussion_logged_notitle(self):
        """
        TEST : Executing a POST request to update a discussion while omitting to specify the title
        Behavior expected : The discussion should not be updated and the user should be redirected back to the discussion creation form.
        """

        # Get a discussion and the associated user
        discussion = models.Discussion.objects.first()
        user = discussion.user

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('update_discussion',kwargs={'slug_discussion':discussion.slug}))
        self.request.user = user

        # Creatng a POST request while omitting the title
        self.request.POST = self.request.POST.copy()
        self.request.POST['topic-name'] = factory.Faker('word').generate({})[:70]
        self.request.POST['title'] = ''
        self.request.POST['language'] = factories.LanguageFactory.create().pk
        
        # Executing the request
        response = CreateUpdateDiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Checking whether no discussion has been created
        self.assertEqual(models.Discussion.objects.count(),self.discussions_count)
        self.assertNotEqual(discussion.title,'')

        # Checking whether the page is unchanged and the user is reaching again the discussion creation form
        self.assertEqual(response.status_code, 200)

    def test_post_update_discussion_logged_valid(self):
        """
        TEST : Executing a POST request to update a discussion (valid request) and the topic are not on the database
        Behavior expected : The discussion should be updated and a  topic should be created if not already existing.
        """
        
        # Get an discussion and the associated user
        discussion = models.Discussion.objects.first()
        user = discussion.user
        previous_topic = discussion.topic
        previous_topic_name = previous_topic.name

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('update_discussion',kwargs={'slug_discussion':discussion.slug}))
        self.request.user = user

        # Creatng a POST request with valid parameters
        self.request.POST = self.request.POST.copy()
        self.request.POST['topic-name'] = factory.Faker('word').generate({})[:70]
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        # Executing the request
        response = CreateUpdateDiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Getting the current instance of the discussion being updated
        discussion = models.Discussion.objects.get(pk=discussion.pk)

        # Assessing that the book has been modified properly
        self.assertEqual(models.Discussion.objects.count(),self.discussions_count)
        self.assertEqual(discussion.title,self.request.POST['title'])
        self.assertEqual(discussion.language.pk,self.request.POST['language'])
        self.assertEqual(previous_topic_name,previous_topic.name)
        self.assertEqual(discussion.topic.name,self.request.POST['topic-name'])

        # Assessing that te user is redirected to the list of discussions
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_discussion'))

class TestDiscussionsListView(TestSupportList,TestCase):
    """
    View with list of discussions
    """

    factory = RequestFactory()
    url_name = 'list_discussion'
    request = factory.get(reverse(url_name))
    supportView = DiscussionsListView
    supportFactory = factories.DiscussionFactory

class TestDetailsDiscussionView(TestCase):
    """
    Details view of one Discussion
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_details_discussion_anonymous(self):
        """
        TEST : Get the details of a discussion without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        discussion = factories.DiscussionFactory.create()
        self.request = self.factory.get(reverse('details_discussion',kwargs={'slug_discussion':discussion.slug}))
        
        self.request.user = AnonymousUser()
        response = DiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_details_discussion_logged_owner(self):
        """
        TEST : Get the details of a discussion a user is owning while being logged
        Behavior expected : The user should access the discussion details
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        discussion = factories.DiscussionFactory.create(user=user)
        self.request = self.factory.get(reverse('details_discussion',kwargs={'slug_discussion':discussion.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = DiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)
    
    def test_details_discussion_logged_not_owner(self):
        """
        TEST : Get the details of an discussion a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        discussion = factories.DiscussionFactory.create()
        self.request = self.factory.get(reverse('details_discussion',kwargs={'slug_discussion':discussion.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = DiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

class TestDeleteDiscussionView(TestCase):
    """
    Delete view of one discussion
    """

    def setUp(self):
        self.factory = RequestFactory()

        # Populate the database with some existing books
        for _ in range(7):
            factories.DiscussionFactory.create()

        self.discussions_count = models.Discussion.objects.count()

    def test_delete_discussion_anonymous(self):
        """
        TEST : Get the delete view of a discussion without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        discussion = models.Discussion.objects.first()
        self.request = self.factory.get(reverse('delete_discussion',kwargs={'slug_discussion':discussion.slug}))
        
        self.request.user = AnonymousUser()
        response = DeleteDiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)
    
    def test_post_delete_discussion_anonymous(self):
        """
        TEST : Post the delete view of a discussion without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        discussion = models.Discussion.objects.first()
        self.request = self.factory.post(reverse('delete_discussion',kwargs={'slug_discussion':discussion.slug}))
        
        self.request.user = AnonymousUser()
        discussions_count_before_delete = models.Discussion.objects.count()
        response = DeleteDiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

        # Checking that the discussion has not been deleted
        self.assertEqual(models.Discussion.objects.count(), discussions_count_before_delete)
        self.assertNotEqual(models.Discussion.objects.filter(pk=discussion.pk).first(), None)

    def test_delete_discussion_logged_owner(self):
        """
        TEST : Get the deletion view of a discussion a user is owning while being logged
        Behavior expected : The user should access the discussion deletion page
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        discussion = factories.DiscussionFactory.create(user=user)
        self.request = self.factory.get(reverse('delete_discussion',kwargs={'slug_discussion':discussion.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = DeleteDiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)

    def test_post_delete_discussion_logged_owner(self):
        """
        TEST : Post the deletion view of a discussion a user is owning while being logged
        Behavior expected : The user should access the discussion deletion page
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        discussion = factories.DiscussionFactory.create(user=user)
        self.request = self.factory.post(reverse('delete_discussion',kwargs={'slug_discussion':discussion.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        discussions_count_before_delete = models.Discussion.objects.count()
        response = DeleteDiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_discussion'))

        # Checking whether the discussion has been deleted
        self.assertEqual(models.Discussion.objects.count(), discussions_count_before_delete-1)
        self.assertEqual(models.Discussion.objects.filter(pk=discussion.pk).first(), None)

    def test_delete_discussion_logged_not_owner(self):
        """
        TEST : Get the deletion view of a discussion a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        discussion = factories.DiscussionFactory.create()
        self.request = self.factory.get(reverse('delete_discussion',kwargs={'slug_discussion':discussion.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = DeleteDiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

    def test_post_delete_discussion_logged_not_owner(self):
        """
        TEST : Post the deletion view of a discussion a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        discussion = factories.DiscussionFactory.create()
        self.request = self.factory.post(reverse('delete_discussion',kwargs={'slug_discussion':discussion.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        discussions_count_before_delete = models.Discussion.objects.count()
        response = DeleteDiscussionView.as_view()(self.request,slug_discussion=discussion.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

        # Checking that the book has not been deleted
        self.assertEqual(models.Discussion.objects.count(), discussions_count_before_delete)
        self.assertNotEqual(models.Discussion.objects.filter(pk=discussion.pk).first(), None)