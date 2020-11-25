import djongo.models as M
from django.db import models
from django.utils import timezone
from time import strftime, gmtime
from django.template.defaultfilters import slugify
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    PermissionManager,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    def create_user(self, email, username):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.save(using=self._db)
        return user


# def song_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'songs/{0}/{1}'.format(strftime('%Y/%m/%d'), generate_file_name() + '.' + filename.split('.')[-1])


class User(AbstractBaseUser):
    _id = M.ObjectIdField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    description = models.TextField()
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


class Song(models.Model):
    _id = M.ObjectIdField(primary_key=True)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Song name")
    slug = models.SlugField(blank=False)
    description = models.CharField(max_length=255)
    cover = models.ImageField(upload_to="covers", blank=False)
    audio = models.FileField(upload_to='audios', blank=False)
    created_at = models.DateTimeField(
        verbose_name='Created At', default=timezone.now)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Song, self).save(*args, **kwargs)


class Playlist(models.Model):
    _id = M.ObjectIdField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='Playlist name')
    slug = models.SlugField(blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ManyToManyField(Song)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Playlist, self).save(*args, **kwargs)
