from django.contrib.auth.models import AbstractUser

# see https://learndjango.com/tutorials/django-custom-user-model

class User(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username
