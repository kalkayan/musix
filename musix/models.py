from django.db import models
import djongo.models as M
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, PermissionManager, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    _id = M.ObjectIdField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
