from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
from .views import *
from . import models
from django.urls import reverse
import factory
from . import factories
from .tests_commons import *

class TestCreateArticleView(TestCase):
    """
    Article creation view
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get(reverse('add_article'))

        # Populate the database with some existing books
        for _ in range(7):
            factories.ArticleFactory.create()

        self.topics_count = models.Topic.objects.count()
        self.newspapers_count = models.Newspaper.objects.count()
        self.articles_count = models.Article.objects.count()

    def test_create_article_anonymous(self):
        """
        TEST : Get the article creation form without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        self.request.user = AnonymousUser()
        response = CreateUpdateArticleView.as_view()(self.request)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_post_create_article_anonymous(self):
        """
        TEST : Post the article creation form without being logged
        Behavior expected : Redirection to the login page
        """

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_article'))
        self.request.user = AnonymousUser()

        # Creatng a POST request while omitting the title
        self.request.POST = self.request.POST.copy()
        self.request.POST['newspaper-name'] = factory.Faker('word')
        self.request.POST['topic-name'] = factory.Faker('word')
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        response = CreateUpdateArticleView.as_view()(self.request)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_get_create_article_logged(self):
        """
        TEST : Get the article creation form while being logged
        Behavior expected : The user should access the article creation page
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        self.request.user = user

        # Executing a HTTP request towards the page
        response = CreateUpdateArticleView.as_view()(self.request)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)

    def test_post_create_article_logged_nonewspaper(self):
        """
        TEST : Executing a POST request to create an article while omitting to specify newspaper's information
        Behavior expected : No article neither newspaper should be created and the user should be redirected back to the article creation form.
        """

        # Create a fake user
        user = factories.UserFactory.create()

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_article'))
        self.request.user = user

        # Creatng a POST request while omitting the author first name
        self.request.POST = self.request.POST.copy()
        self.request.POST['newspaper-name'] = ''
        self.request.POST['topic-name'] = factory.Faker('word')
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        # Executing the request
        response = CreateUpdateArticleView.as_view()(self.request)

        # Checking whether no author neither book has been created
        self.assertEqual(models.Newspaper.objects.count(),self.newspapers_count)
        # self.assertEqual(models.Topic.objects.count(),self.topics_count) > cannot topic shared with other tables
        self.assertEqual(models.Article.objects.count(),self.articles_count)

        # Checking whether the page is unchanged and the user is reaching again the book creation form
        self.assertEqual(response.status_code, 200)

    def test_post_create_article_logged_notopic(self):
        """
        TEST : Executing a POST request to create an article while omitting to specify topic's information
        Behavior expected : No article neither topic should be created and the user should be redirected back to the article creation form.
        """

        # Create a fake user
        user = factories.UserFactory.create()

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_article'))
        self.request.user = user

        # Creatng a POST request while omitting the author first name
        self.request.POST = self.request.POST.copy()
        self.request.POST['newspaper-name'] = factory.Faker('word')
        self.request.POST['topic-name'] = ''
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        # Executing the request
        response = CreateUpdateArticleView.as_view()(self.request)

        # Checking whether no author neither book has been created
        self.assertEqual(models.Newspaper.objects.count(),self.newspapers_count)
        self.assertEqual(models.Topic.objects.count(),self.topics_count)
        self.assertEqual(models.Article.objects.count(),self.articles_count)

        # Checking whether the page is unchanged and the user is reaching again the book creation form
        self.assertEqual(response.status_code, 200)

    def test_post_create_article_logged_notitle(self):
        """
        TEST : Executing a POST request to create a book while omitting to specify the title
        Behavior expected : No article neither newspaper, topic should be created and the user should be redirected back to the book creation form.
        """

        # Create a fake user
        user = factories.UserFactory.create()

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_article'))
        self.request.user = user

        # Creatng a POST request while omitting the title
        self.request.POST = self.request.POST.copy()
        self.request.POST['newspaper-name'] = factory.Faker('word')
        self.request.POST['topic-name'] = factory.Faker('word')
        self.request.POST['title'] = ''
        self.request.POST['language'] = factories.LanguageFactory.create().pk
        
        # Executing the request
        response = CreateUpdateArticleView.as_view()(self.request)

        # Checking whether no author neither book has been created
        self.assertEqual(models.Article.objects.count(),self.articles_count)
        # self.assertEqual(models.Topic.objects.count(),self.topics_count) > cannot topic shared with other tables
        self.assertEqual(models.Newspaper.objects.count(),self.newspapers_count)

        # Checking whether the page is unchanged and the user is reaching again the book creation form
        self.assertEqual(response.status_code, 200)

    def test_post_create_article_logged_valid_not_existing_newspaper_topic(self):
        """
        TEST : Executing a POST request to create an article (valid request) and the newspaper/topic is not on the database
        Behavior expected : An article, a topic and a newspaper should be created
        """
        
        # Create a fake user
        user = factories.UserFactory.create()

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_article'))
        self.request.user = user

        # Creatng a POST request with valid parameters
        self.request.POST = self.request.POST.copy()
        self.request.POST['newspaper-name'] = factory.Faker('word')
        self.request.POST['topic-name'] = factory.Faker('word')
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        # Executing the request
        response = CreateUpdateArticleView.as_view()(self.request)

        # Assessing that both a book and an author have been created
        self.assertEqual(models.Newspaper.objects.count(),self.newspapers_count+1)
        self.assertEqual(models.Topic.objects.count(),self.topics_count+1)
        self.assertEqual(models.Article.objects.count(),self.articles_count+1)

        # Assessing that te user is redirected to the list of books
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_article'))

    def test_post_create_article_logged_valid_existing_newspaper_topic(self):
        """
        TEST : Executing a POST request to create an article (valid request) and the newspaper, topic are already on the database
        Behavior expected : An article should be created but no newspaper,topic should be created (just a reference to it)
        """
        
        user = factories.UserFactory.create()

        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_article'))
        self.request.user = user
        self.request.POST = self.request.POST.copy()

        newspaper = models.Newspaper.objects.first()
        topic = models.Topic.objects.first()
        self.request.POST['newspaper-name'] = newspaper.name
        self.request.POST['topic-name'] = topic.name
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk
        response = CreateUpdateArticleView.as_view()(self.request)

        # Checking whether an article is created but no newspaper/topic
        self.assertEqual(models.Newspaper.objects.count(),self.newspapers_count)
        self.assertEqual(models.Topic.objects.count(),self.topics_count)
        self.assertEqual(models.Article.objects.count(),self.articles_count+1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_article'))

class TestUpdateArticleView(TestCase):
    """
    Article update view
    """

    def setUp(self):
        self.factory = RequestFactory()

        # Populate the database with some existing books
        for _ in range(7):
            factories.ArticleFactory.create()

        self.topics_count = models.Topic.objects.count()
        self.newspapers_count = models.Newspaper.objects.count()
        self.articles_count = models.Article.objects.count()

    def test_update_article_anonymous(self):
        """
        TEST : Update an article without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        article = models.Article.objects.first()
        self.request = self.factory.get(reverse('update_article',kwargs={'slug_article':article.slug}))
        
        self.request.user = AnonymousUser()
        response = CreateUpdateArticleView.as_view()(self.request,slug_article=article.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_post_update_article_anonymous(self):
        """
        TEST : Update an article without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        article = models.Article.objects.first()
        self.request = self.factory.post(reverse('update_article',kwargs={'slug_article':article.slug}))
        
        # Configuring the POST request with valid parameters
        self.request.POST = self.request.POST.copy()
        self.request.POST['newspaper-name'] = factory.Faker('word')
        self.request.POST['topic-name'] = factory.Faker('word')
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        self.request.user = AnonymousUser()
        response = CreateUpdateArticleView.as_view()(self.request,slug_article=article.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_update_article_logged_owner(self):
        """
        TEST : Update an article a user is owning while being logged
        Behavior expected : The user should access the article update form
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        article = factories.ArticleFactory.create(user=user)
        self.request = self.factory.get(reverse('update_article',kwargs={'slug_article':article.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = CreateUpdateArticleView.as_view()(self.request,slug_article=article.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)
    
    def test_update_article_logged_not_owner(self):
        """
        TEST : Update an article a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        article = models.Article.objects.first()
        self.request = self.factory.get(reverse('update_article',kwargs={'slug_article':article.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = CreateUpdateArticleView.as_view()(self.request,slug_article=article.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

    def test_post_update_article_logged_not_owner(self):
        """
        TEST : Update an article a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        article = models.Article.objects.first()
        self.request = self.factory.post(reverse('update_article',kwargs={'slug_article':article.slug}))
        self.request.user = user

         # Configuring the POST request with valid parameters
        self.request.POST = self.request.POST.copy()
        self.request.POST['newspaper-name'] = factory.Faker('word')
        self.request.POST['topic-name'] = factory.Faker('word')
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        # Executing a HTTP request towards the page
        response = CreateUpdateArticleView.as_view()(self.request,slug_article=article.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

    def test_post_update_article_logged_notitle(self):
        """
        TEST : Executing a POST request to update an article while omitting to specify the title
        Behavior expected : The article should not be updated and the user should be redirected back to the book creation form.
        """

        # Get an article and the associated user
        article = models.Article.objects.first()
        user = article.user

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('update_article',kwargs={'slug_article':article.slug}))
        self.request.user = user

        # Creatng a POST request while omitting the title
        self.request.POST = self.request.POST.copy()
        self.request.POST['newspaper-name'] = factory.Faker('word')
        self.request.POST['topic-name'] = factory.Faker('word')
        self.request.POST['title'] = ''
        self.request.POST['language'] = factories.LanguageFactory.create().pk
        
        # Executing the request
        response = CreateUpdateArticleView.as_view()(self.request,slug_article=article.slug)

        # Checking whether no article has been created
        self.assertEqual(models.Article.objects.count(),self.articles_count)
        self.assertNotEqual(article.title,'')

        # Checking whether the page is unchanged and the user is reaching again the book creation form
        self.assertEqual(response.status_code, 200)

    def test_post_update_article_logged_valid(self):
        """
        TEST : Executing a POST request to update an article (valid request) and the topic, newspaper are not on the database
        Behavior expected : The book should be updated and a newspaper, topic should be created if not already existing.
        """
        
        # Get an article and the associated user
        article = models.Article.objects.first()
        user = article.user
        previous_newspaper = article.newspaper
        previous_topic = article.topic
        previous_newspaper_name = previous_newspaper.name
        previous_topic_name = previous_topic.name

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('update_article',kwargs={'slug_article':article.slug}))
        self.request.user = user

        # Creatng a POST request with valid parameters
        self.request.POST = self.request.POST.copy()
        self.request.POST['newspaper-name'] = factory.Faker('word').generate({})
        self.request.POST['topic-name'] = factory.Faker('word').generate({})
        self.request.POST['title'] = factory.Faker('sentence').generate({})[:70]
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        # Executing the request
        response = CreateUpdateArticleView.as_view()(self.request,slug_article=article.slug)

        # Getting the current instance of the article being updated
        article = models.Article.objects.get(pk=article.pk)

        # Assessing that the book has been modified properly
        self.assertEqual(models.Article.objects.count(),self.articles_count)
        self.assertEqual(article.title,self.request.POST['title'])
        self.assertEqual(article.language.pk,self.request.POST['language'])
        self.assertEqual(previous_newspaper_name,previous_newspaper.name)
        self.assertEqual(previous_topic_name,previous_topic.name)
        self.assertEqual(article.newspaper.name,self.request.POST['newspaper-name'])
        self.assertEqual(article.topic.name,self.request.POST['topic-name'])

        # Assessing that te user is redirected to the list of books
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_article'))

class TestArticlesListView(TestSupportList,TestCase):
    """
    View with list of articles
    """

    factory = RequestFactory()
    url_name = 'list_article'
    request = factory.get(reverse(url_name))
    supportView = ArticlesListView
    supportFactory = factories.ArticleFactory

class TestDetailsArticleView(TestCase):
    """
    Details view of one Article
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_details_article_anonymous(self):
        """
        TEST : Get the details of an article without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        article = factories.ArticleFactory.create()
        self.request = self.factory.get(reverse('details_article',kwargs={'slug_article':article.slug}))
        
        self.request.user = AnonymousUser()
        response = ArticleView.as_view()(self.request,slug_article=article.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_details_article_logged_owner(self):
        """
        TEST : Get the details of an article a user is owning while being logged
        Behavior expected : The user should access the book details
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        article = factories.ArticleFactory.create(user=user)
        self.request = self.factory.get(reverse('details_article',kwargs={'slug_article':article.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = ArticleView.as_view()(self.request,slug_article=article.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)
    
    def test_details_article_logged_not_owner(self):
        """
        TEST : Get the details of an article a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        article = factories.ArticleFactory.create()
        self.request = self.factory.get(reverse('details_article',kwargs={'slug_article':article.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = ArticleView.as_view()(self.request,slug_article=article.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

class TestDeleteArticleView(TestCase):
    """
    Delete view of one Article
    """

    def setUp(self):
        self.factory = RequestFactory()

        # Populate the database with some existing books
        for _ in range(7):
            factories.ArticleFactory.create()

        self.articles_count = models.Article.objects.count()

    def test_delete_article_anonymous(self):
        """
        TEST : Get the delete view of an article without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        article = models.Article.objects.first()
        self.request = self.factory.get(reverse('delete_article',kwargs={'slug_article':article.slug}))
        
        self.request.user = AnonymousUser()
        response = DeleteArticleView.as_view()(self.request,slug_article=article.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)
    
    def test_post_delete_article_anonymous(self):
        """
        TEST : Post the delete view of an article without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        article = models.Article.objects.first()
        self.request = self.factory.post(reverse('delete_article',kwargs={'slug_article':article.slug}))
        
        self.request.user = AnonymousUser()
        articles_count_before_delete = models.Article.objects.count()
        response = DeleteArticleView.as_view()(self.request,slug_article=article.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

        # Checking that the book has not been deleted
        self.assertEqual(models.Article.objects.count(), articles_count_before_delete)
        self.assertNotEqual(models.Article.objects.filter(pk=article.pk).first(), None)

    def test_delete_article_logged_owner(self):
        """
        TEST : Get the deletion view of an article a user is owning while being logged
        Behavior expected : The user should access the article deletion page
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        article = factories.ArticleFactory.create(user=user)
        self.request = self.factory.get(reverse('delete_article',kwargs={'slug_article':article.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = DeleteArticleView.as_view()(self.request,slug_article=article.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)

    def test_post_delete_article_logged_owner(self):
        """
        TEST : Post the deletion view of an article a user is owning while being logged
        Behavior expected : The user should access the article deletion page
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        article = factories.ArticleFactory.create(user=user)
        self.request = self.factory.post(reverse('delete_article',kwargs={'slug_article':article.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        articles_count_before_delete = models.Article.objects.count()
        response = DeleteArticleView.as_view()(self.request,slug_article=article.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_article'))

        # Checking whether the book has been deleted
        self.assertEqual(models.Article.objects.count(), articles_count_before_delete-1)
        self.assertEqual(models.Article.objects.filter(pk=article.pk).first(), None)

    def test_delete_article_logged_not_owner(self):
        """
        TEST : Get the deletion view of an article a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        article = factories.ArticleFactory.create()
        self.request = self.factory.get(reverse('delete_article',kwargs={'slug_article':article.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = DeleteArticleView.as_view()(self.request,slug_article=article.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

    def test_post_delete_article_logged_not_owner(self):
        """
        TEST : Post the deletion view of an article a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        article = factories.ArticleFactory.create()
        self.request = self.factory.post(reverse('delete_article',kwargs={'slug_article':article.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        articles_count_before_delete = models.Article.objects.count()
        response = DeleteArticleView.as_view()(self.request,slug_article=article.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

        # Checking that the book has not been deleted
        self.assertEqual(models.Article.objects.count(), articles_count_before_delete)
        self.assertNotEqual(models.Article.objects.filter(pk=article.pk).first(), None)