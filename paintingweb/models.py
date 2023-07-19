from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # Delete not use field
    first_name = None
    last_name = None
    username = None
    last_login = None
    is_staff = None
    is_superuser = None

    # username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True, null=True)
    password = models.CharField(max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email   

class Artist(models.Model):
    fullname = models.CharField(
        max_length=50,
        null=True
    )
    bio = models.TextField(null=True)
    gender = models.BooleanField(null=True)
    age = models.IntegerField(null=True)
    dateofbirth = models.DateTimeField(null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        null=True
    )

    def __str__(self):
        return self.fullname


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    artwork = models.ForeignKey(
        "Artwork",
        on_delete=models.CASCADE
    )


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    artwork = models.ForeignKey(
        "Artwork",
        on_delete=models.CASCADE
    )


class Artwork(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    link = models.CharField(max_length=200, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )
    author = models.ForeignKey(
        Artist,
        on_delete=models.DO_NOTHING,
        null=True
    )
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.name
        
    def favored_by(self):
        return Favorite.objects.filter(artwork_id=self.id)

    def bookmarked_by(self):
        return Bookmark.objects.filter(artwork_id=self.id)


