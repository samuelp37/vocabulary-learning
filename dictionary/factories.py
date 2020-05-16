import factory
from django.contrib.auth.models import User
from . import models
import random
from faker.providers import BaseProvider
from faker import Faker

fake_gender = Faker()
class GenderProvider(BaseProvider):
    def gender(self):
        correspondences = {"M":"Masculine","F":"Feminine","N":"Neutral","-":"-"}
        shorts = [short for short in correspondences]
        chosen = random.choice(shorts)
        long_gender = correspondences[chosen]
        return chosen,long_gender
fake_gender.add_provider(GenderProvider)

class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Language
    name = random.choices(["French","English","German"])

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('email')

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Author
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Topic
    name = factory.Faker('word')

class NewspaperFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Newspaper
    name = factory.Faker('word')

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Book
    author = factory.SubFactory(AuthorFactory)
    title = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    language = factory.SubFactory(LanguageFactory)
    slug = factory.Faker('slug')

class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Article
    newspaper = factory.SubFactory(NewspaperFactory)
    topic = factory.SubFactory(TopicFactory)
    title = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    language = factory.SubFactory(LanguageFactory)
    slug = factory.Faker('slug')

class DiscussionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Discussion
    topic = factory.SubFactory(TopicFactory)
    title = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    language = factory.SubFactory(LanguageFactory)
    slug = factory.Faker('slug')

class GenderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Gender
    short, gender = fake_gender.gender()

class WordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Word
    word = factory.Faker('word')
    plural = factory.Faker('word')
    gender = factory.SubFactory(GenderFactory)
    language = factory.SubFactory(LanguageFactory)

class AdjectiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Adjective
    word = factory.Faker('word')
    plural = factory.Faker('word')
    language = factory.SubFactory(LanguageFactory)

class VerbFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Verb
    word = factory.Faker('word')
    language = factory.SubFactory(LanguageFactory)

class ExpressionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Expression
    expression = factory.Faker('sentence')
    language = factory.SubFactory(LanguageFactory)

class TranslationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Translation
    original_word = factory.SubFactory(WordFactory)
    translated_word = factory.SubFactory(WordFactory)
    original_adj = factory.SubFactory(AdjectiveFactory)
    translated_adj = factory.SubFactory(AdjectiveFactory)
    original_verb = factory.SubFactory(VerbFactory)
    translated_verb = factory.SubFactory(VerbFactory)
    original_exp = factory.SubFactory(ExpressionFactory)
    translated_exp = factory.SubFactory(ExpressionFactory)
    date_added = factory.Faker('date')
    context_sentence = ""
    translation_context_sentence = ""
    slug = factory.Faker('slug')
    user = factory.SubFactory(UserFactory)