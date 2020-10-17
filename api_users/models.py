from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRoles:
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    choices = (
        (USER, USER),
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
    )


class User(AbstractUser):
    email = models.EmailField('email', unique=True)
    first_name = models.CharField('first name', max_length=40, blank=True)
    last_name = models.CharField('last name', max_length=40, blank=True)
    bio = models.TextField('bio', blank=True)
    role = models.CharField(max_length=9,
                            choices=UserRoles.choices,
                            default=UserRoles.USER)

    def __str__(self):
        return self.username
