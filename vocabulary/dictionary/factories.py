import factory
from django.contrib.auth.models import User

class UserFactoryEmpty(factory.Factory):
    class Meta:
        model = User

    first_name = 'User'
    last_name = 'NoAdmin'

class UserFactoryFull(factory.Factory):
    class Meta:
        model = User

    # TODO : Create a complete profile