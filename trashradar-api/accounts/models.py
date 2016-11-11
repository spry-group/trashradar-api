from __future__ import unicode_literals

from django.contrib.auth import models as auth_models
from django.db import models


class AccountManager(auth_models.BaseUserManager):
    """
    Custom User Manager which inherits from BaseUserManager
    """

    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email, name
        and password.
        :param email: User email
        :param password: User password
        :param kwargs: Extra args
        :return: User's model instance
        """
        if not email:
            raise ValueError('Users must have an email address')

        if 'username' not in kwargs:
            username = self.normalize_email(email)
        else:
            username = kwargs['username']
        del kwargs['username']

        account = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs
        )
        account.set_password(password)
        account.is_active = True
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        :param email: User email
        :param password: User password
        :param kwargs: Extra args
        :return: User's model instance
        """
        account = self.create_user(email, password, **kwargs)
        account.is_active = True
        account.is_verified = True
        account.is_staff = True
        account.is_superuser = True
        account.save()

        return account


class Account(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    """
    Custom User model which inherits from AbstractBaseUser
    """
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        """
        :return: Username
        """
        return self.username

    def get_full_name(self):
        """
        :return: Full name
        """
        return self.full_name

    def get_short_name(self):
        """
        :return: Fist name
        """
        return self.full_name
