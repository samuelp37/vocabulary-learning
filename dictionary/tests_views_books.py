from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
from .views import *
from . import models
from django.urls import reverse
import factory
from . import factories
from .tests_commons import *

class TestCreateBookView(TestCase):
    """
    Book creation view
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get(reverse('add_book'))

        # Populate the database with some existing books
        for _ in range(7):
            factories.BookFactory.create()

        self.authors_count = models.Author.objects.count()
        self.books_count = models.Book.objects.count()

    def test_create_book_anonymous(self):
        """
        TEST : Get the book creation form without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        self.request.user = AnonymousUser()
        response = CreateUpdateBookView.as_view()(self.request)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_post_create_book_anonymous(self):
        """
        TEST : Post the book creation form without being logged
        Behavior expected : Redirection to the login page
        """

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_book'))
        self.request.user = AnonymousUser()

        # Creatng a POST request while omitting the title
        self.request.POST = self.request.POST.copy()
        self.request.POST['author-first_name'] = factory.Faker('first_name')
        self.request.POST['author-last_name'] = factory.Faker('last_name')
        self.request.POST['title'] = factory.Faker('sentence')
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        response = CreateUpdateBookView.as_view()(self.request)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_get_create_book_logged(self):
        """
        TEST : Get the book creation form while being logged
        Behavior expected : The user should access the book creation page
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        self.request.user = user

        # Executing a HTTP request towards the page
        response = CreateUpdateBookView.as_view()(self.request)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)

    def test_post_create_book_logged_noauthor_firstname(self):
        """
        TEST : Executing a POST request to create a book while omitting to specify author's information
        Behavior expected : No book neither author should be created and the user should be redirected back to the book creation form.
        """

        # Create a fake user
        user = factories.UserFactory.create()

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_book'))
        self.request.user = user

        # Creatng a POST request while omitting the author first name
        self.request.POST = self.request.POST.copy()
        self.request.POST['author-first_name'] = ''
        self.request.POST['author-last_name'] = factory.Faker('last_name')
        self.request.POST['title'] = factory.Faker('sentence')
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        # Executing the request
        response = CreateUpdateBookView.as_view()(self.request)

        # Checking whether no author neither book has been created
        self.assertEqual(models.Author.objects.count(),self.authors_count)
        self.assertEqual(models.Book.objects.count(),self.books_count)

        # Checking whether the page is unchanged and the user is reaching again the book creation form
        self.assertEqual(response.status_code, 200)

    def test_post_create_book_logged_notitle(self):
        """
        TEST : Executing a POST request to create a book while omitting to specify the title
        Behavior expected : No book neither author should be created and the user should be redirected back to the book creation form.
        """

        # Create a fake user
        user = factories.UserFactory.create()

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_book'))
        self.request.user = user

        # Creatng a POST request while omitting the title
        self.request.POST = self.request.POST.copy()
        self.request.POST['author-first_name'] = factory.Faker('first_name')
        self.request.POST['author-last_name'] = factory.Faker('last_name')
        self.request.POST['title'] = ''
        self.request.POST['language'] = factories.LanguageFactory.create().pk
        
        # Executing the request
        response = CreateUpdateBookView.as_view()(self.request)

        # Checking whether no author neither book has been created
        self.assertEqual(models.Book.objects.count(),self.books_count)
        self.assertEqual(models.Author.objects.count(),self.authors_count)

        # Checking whether the page is unchanged and the user is reaching again the book creation form
        self.assertEqual(response.status_code, 200)

    def test_post_create_book_logged_valid_not_existing_author(self):
        """
        TEST : Executing a POST request to create a book (valid request) and the author is not on the database
        Behavior expected : A book and an author should be created
        """
        
        # Create a fake user
        user = factories.UserFactory.create()

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_book'))
        self.request.user = user

        # Creatng a POST request with valid parameters
        self.request.POST = self.request.POST.copy()
        self.request.POST['author-first_name'] = factory.Faker('first_name')
        self.request.POST['author-last_name'] = factory.Faker('last_name')
        self.request.POST['title'] = factory.Faker('sentence')
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        # Executing the request
        response = CreateUpdateBookView.as_view()(self.request)

        # Assessing that both a book and an author have been created
        self.assertEqual(models.Author.objects.count(),self.authors_count+1)
        self.assertEqual(models.Book.objects.count(),self.books_count+1)

        # Assessing that te user is redirected to the list of books
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_book'))

    def test_post_create_book_logged_valid_existing_author(self):
        """
        TEST : Executing a POST request to create a book (valid request) and the author is already on the database
        Behavior expected : A book should be created but no author should be created (just a reference to it)
        """
        
        user = factories.UserFactory.create()

        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('add_book'))
        self.request.user = user
        self.request.POST = self.request.POST.copy()

        author = models.Author.objects.first()
        self.request.POST['author-first_name'] = author.first_name
        self.request.POST['author-last_name'] = author.last_name
        self.request.POST['title'] = factory.Faker('sentence')
        self.request.POST['language'] = factories.LanguageFactory.create().pk
        response = CreateUpdateBookView.as_view()(self.request)

        # Checking whether the user with no activity does not really see any translation
        self.assertEqual(models.Author.objects.count(),self.authors_count)
        self.assertEqual(models.Book.objects.count(),self.books_count+1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_book'))

class TestUpdateBookView(TestCase):
    """
    Book creation view
    """

    def setUp(self):
        self.factory = RequestFactory()

        # Populate the database with some existing books
        for _ in range(7):
            factories.BookFactory.create()

        self.authors_count = models.Author.objects.count()
        self.books_count = models.Book.objects.count()

    def test_update_book_anonymous(self):
        """
        TEST : Update a book without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        book = models.Book.objects.first()
        self.request = self.factory.get(reverse('update_book',kwargs={'slug_book':book.slug}))
        
        self.request.user = AnonymousUser()
        response = CreateUpdateBookView.as_view()(self.request,slug_book=book.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_post_update_book_anonymous(self):
        """
        TEST : Update a book without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        book = models.Book.objects.first()
        self.request = self.factory.post(reverse('update_book',kwargs={'slug_book':book.slug}))
        
        # Configuring the POST request with valid parameters
        self.request.POST = self.request.POST.copy()
        self.request.POST['author-first_name'] = factory.Faker('first_name')
        self.request.POST['author-last_name'] = factory.Faker('last_name')
        self.request.POST['title'] = factory.Faker('sentence')
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        self.request.user = AnonymousUser()
        response = CreateUpdateBookView.as_view()(self.request,slug_book=book.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_update_book_logged_owner(self):
        """
        TEST : Update a book a user is owning while being logged
        Behavior expected : The user should access the book update form
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        book = factories.BookFactory.create(user=user)
        self.request = self.factory.get(reverse('update_book',kwargs={'slug_book':book.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = CreateUpdateBookView.as_view()(self.request,slug_book=book.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)
    
    def test_update_book_logged_not_owner(self):
        """
        TEST : Update a book a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        book = models.Book.objects.first()
        self.request = self.factory.get(reverse('update_book',kwargs={'slug_book':book.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = CreateUpdateBookView.as_view()(self.request,slug_book=book.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

    def test_post_update_book_logged_not_owner(self):
        """
        TEST : Update a book a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        book = models.Book.objects.first()
        self.request = self.factory.post(reverse('update_book',kwargs={'slug_book':book.slug}))
        self.request.user = user

         # Configuring the POST request with valid parameters
        self.request.POST = self.request.POST.copy()
        self.request.POST['author-first_name'] = factory.Faker('first_name')
        self.request.POST['author-last_name'] = factory.Faker('last_name')
        self.request.POST['title'] = factory.Faker('sentence')
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        # Executing a HTTP request towards the page
        response = CreateUpdateBookView.as_view()(self.request,slug_book=book.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

    def test_post_update_book_logged_notitle(self):
        """
        TEST : Executing a POST request to update a book while omitting to specify the title
        Behavior expected : The book should not be updated and the user should be redirected back to the book creation form.
        """

        # Get a book and the associated user
        book = models.Book.objects.first()
        user = book.user

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('update_book',kwargs={'slug_book':book.slug}))
        self.request.user = user

        # Creatng a POST request while omitting the title
        self.request.POST = self.request.POST.copy()
        self.request.POST['author-first_name'] = factory.Faker('first_name')
        self.request.POST['author-last_name'] = factory.Faker('last_name')
        self.request.POST['title'] = ''
        self.request.POST['language'] = factories.LanguageFactory.create().pk
        
        # Executing the request
        response = CreateUpdateBookView.as_view()(self.request,slug_book=book.slug)

        # Checking whether no book has been created
        self.assertEqual(models.Book.objects.count(),self.books_count)
        self.assertNotEqual(book.title,'')

        # Checking whether the page is unchanged and the user is reaching again the book creation form
        self.assertEqual(response.status_code, 200)

    def test_post_update_book_logged_valid(self):
        """
        TEST : Executing a POST request to update a book (valid request) and the author is not on the database
        Behavior expected : The book should be updated and an author should be created if not already existing.
        """
        
        # Get a book and the associated user
        book = models.Book.objects.first()
        user = book.user
        previous_author = book.author
        previous_first_name = previous_author.first_name
        previous_last_name = previous_author.last_name

        # Preparing the request and identify as the user
        self.factory = RequestFactory()
        self.request = self.factory.post(reverse('update_book',kwargs={'slug_book':book.slug}))
        self.request.user = user

        # Creatng a POST request with valid parameters
        self.request.POST = self.request.POST.copy()
        self.request.POST['author-first_name'] = factory.Faker('first_name').generate({})
        self.request.POST['author-last_name'] = factory.Faker('last_name').generate({})
        self.request.POST['title'] = factory.Faker('sentence').generate({})
        self.request.POST['language'] = factories.LanguageFactory.create().pk

        # Executing the request
        response = CreateUpdateBookView.as_view()(self.request,slug_book=book.slug)

        # Getting the current instance of the book being updated
        book = models.Book.objects.get(pk=book.pk)

        # Assessing that the book has been modified properly
        self.assertEqual(models.Book.objects.count(),self.books_count)
        self.assertEqual(book.title,self.request.POST['title'])
        self.assertEqual(book.language.pk,self.request.POST['language'])
        self.assertEqual(previous_first_name,previous_author.first_name)
        self.assertEqual(previous_last_name,previous_author.last_name)
        self.assertEqual(book.author.first_name,self.request.POST['author-first_name'])
        self.assertEqual(book.author.last_name,self.request.POST['author-last_name'])

        # Assessing that te user is redirected to the list of books
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_book'))

class TestBooksListView(TestSupportList,TestCase):
    """
    View with list of books
    """

    factory = RequestFactory()
    url_name = 'list_book'
    request = factory.get(reverse(url_name))
    supportView = BooksListView
    supportFactory = factories.BookFactory

class TestDetailsBookView(TestCase):
    """
    Details view of one Book
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_details_book_anonymous(self):
        """
        TEST : Get the details of a book without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        book = factories.BookFactory.create()
        self.request = self.factory.get(reverse('details_book',kwargs={'slug_book':book.slug}))
        
        self.request.user = AnonymousUser()
        response = BookView.as_view()(self.request,slug_book=book.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

    def test_details_book_logged_owner(self):
        """
        TEST : Get the details of a book a user is owning while being logged
        Behavior expected : The user should access the book details
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        book = factories.BookFactory.create(user=user)
        self.request = self.factory.get(reverse('details_book',kwargs={'slug_book':book.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = BookView.as_view()(self.request,slug_book=book.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)
    
    def test_details_book_logged_not_owner(self):
        """
        TEST : Get the details of a book a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        book = factories.BookFactory.create()
        self.request = self.factory.get(reverse('details_book',kwargs={'slug_book':book.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = BookView.as_view()(self.request,slug_book=book.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

class TestDeleteBookView(TestCase):
    """
    Delete view of one Book
    """

    def setUp(self):
        self.factory = RequestFactory()

        # Populate the database with some existing books
        for _ in range(7):
            factories.BookFactory.create()

        self.books_count = models.Book.objects.count()

    def test_delete_book_anonymous(self):
        """
        TEST : Get the delete view of a book without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        book = models.Book.objects.first()
        self.request = self.factory.get(reverse('delete_book',kwargs={'slug_book':book.slug}))
        
        self.request.user = AnonymousUser()
        response = DeleteBookView.as_view()(self.request,slug_book=book.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)
    
    def test_post_delete_book_anonymous(self):
        """
        TEST : Post the delete view of a book without being logged
        Behavior expected : Redirection to the login page
        """

        # Executing the page request with a Anonymous User
        book = models.Book.objects.first()
        self.request = self.factory.post(reverse('delete_book',kwargs={'slug_book':book.slug}))
        
        self.request.user = AnonymousUser()
        books_count_before_delete = models.Book.objects.count()
        response = DeleteBookView.as_view()(self.request,slug_book=book.slug)

        # Assert redirection to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login",response.url)

        # Checking that the book has not been deleted
        self.assertEqual(models.Book.objects.count(), books_count_before_delete)
        self.assertNotEqual(models.Book.objects.filter(pk=book.pk).first(), None)

    def test_delete_book_logged_owner(self):
        """
        TEST : Get the deletion view of a book a user is owning while being logged
        Behavior expected : The user should access the book deletion page
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        book = factories.BookFactory.create(user=user)
        self.request = self.factory.get(reverse('delete_book',kwargs={'slug_book':book.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = DeleteBookView.as_view()(self.request,slug_book=book.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 200)

    def test_post_delete_book_logged_owner(self):
        """
        TEST : Post the deletion view of a book a user is owning while being logged
        Behavior expected : The user should access the book deletion page
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        book = factories.BookFactory.create(user=user)
        self.request = self.factory.post(reverse('delete_book',kwargs={'slug_book':book.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        books_count_before_delete = models.Book.objects.count()
        response = DeleteBookView.as_view()(self.request,slug_book=book.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list_book'))

        # Checking whether the book has been deleted
        self.assertEqual(models.Book.objects.count(), books_count_before_delete-1)
        self.assertEqual(models.Book.objects.filter(pk=book.pk).first(), None)

    def test_delete_book_logged_not_owner(self):
        """
        TEST : Get the deletion view of a book a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        book = factories.BookFactory.create()
        self.request = self.factory.get(reverse('delete_book',kwargs={'slug_book':book.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        response = DeleteBookView.as_view()(self.request,slug_book=book.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

    def test_post_delete_book_logged_not_owner(self):
        """
        TEST : Post the deletion view of a book a user is not owning while being logged
        Behavior expected : The user should have a forbidden access
        """

        # Simulate a user and perform a request
        user = factories.UserFactory.create()
        book = factories.BookFactory.create()
        self.request = self.factory.post(reverse('delete_book',kwargs={'slug_book':book.slug}))
        self.request.user = user

        # Executing a HTTP request towards the page
        books_count_before_delete = models.Book.objects.count()
        response = DeleteBookView.as_view()(self.request,slug_book=book.slug)

        # Assessing whether the user indeed accesses the page
        self.assertEqual(response.status_code, 403)

        # Checking that the book has not been deleted
        self.assertEqual(models.Book.objects.count(), books_count_before_delete)
        self.assertNotEqual(models.Book.objects.filter(pk=book.pk).first(), None)