from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

from user.managers import UserManager


class BlogUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    # first_blog = models.ForeignKey(Blog, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def __str__(self):
        return "{} {} {}".format(self.first_name, self.last_name, self.email)

    def save(self, *args, **kwargs):
        self.username = self.email
        return super(BlogUser, self).save(*args, **kwargs)


