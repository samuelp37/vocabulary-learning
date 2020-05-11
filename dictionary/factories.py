import factory
from django.contrib.auth.models import User
from .models import Book, Author, Language
import random

class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Language
    name = random.choice(["French","English","German"])

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('email')

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
    author = factory.SubFactory(AuthorFactory)
    title = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    language = factory.SubFactory(LanguageFactory)