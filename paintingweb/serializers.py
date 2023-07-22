from dataclasses import fields
from typing_extensions import Required
from wsgiref.validate import validator
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from email.headerregistry import Address
from django.contrib.auth.password_validation import validate_password
from . import models


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Add extra responses here
        artist = models.Artist.objects.get(user=self.user)
        data['id'] = self.user.id
        data['name'] = artist.fullname or ""
        data['email'] = self.user.email
        return data


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(
        'connectedProfile', read_only=True)

    def connectedProfile(self, userItem):
        return ArtistSerializer(userItem.profile()).data

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'groups', 'profile']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=models.User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    name = serializers.CharField(
        required=False,
        write_only=True,
        validators=[]
    )

    class Meta:
        model = models.User
        fields = ('email', 'password', 'name')

    def create(self, validated_data):
        userEmail = validated_data['email']
        userId = Address(addr_spec=userEmail).username
        userName = ""
        try:
            userName = validated_data['name']
        except KeyError as ke:
            pass

        user = models.User.objects.create(
            id=userId,
            email=userEmail,
        )
        user.set_password(validated_data['password'])
        user.save()
        artist = models.Artist.objects.create(
            fullname=userName,
            user=user
        )
        artist.save()

        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class ArtistSerializer(serializers.ModelSerializer):
    artworks = serializers.SerializerMethodField('artworkList', read_only=True)

    def artworkList(self, artistItem):
        return ArtworkSerializer(artistItem.artworks(), many=True).data

    class Meta:
        model = models.Artist
        fields = ['id', 'fullname', 'bio', 'gender',
                  'age', 'dateofbirth', 'artworks', 'user']


class CategorySerializer(serializers.ModelSerializer):
    background = serializers.SerializerMethodField(
        'featured_artwork', read_only=True)
    number_of_artworks = serializers.SerializerMethodField(
        'count_artwork', read_only=True)

    def featured_artwork(self, categoryItem):
        return categoryItem.background().link if categoryItem.background() else None

    def count_artwork(self, categoryItem):
        return categoryItem.number_of_artworks()

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'background', 'number_of_artworks']


class ArtworkSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField('get_category')
    author_email = serializers.SerializerMethodField('get_author')
    favored_by = serializers.SerializerMethodField('favorite_by')
    bookmarked_by = serializers.SerializerMethodField('bookmark_by')

    def favorite_by(self, artworkItem):
        return FavoriteSerializer(artworkItem.favored_by(), many=True).data

    def bookmark_by(self, artworkItem):
        return BookmarkSerializer(artworkItem.bookmarked_by(), many=True).data

    def get_category(self, artworkItem):
        kate = None
        try:
            kate = models.Category.objects.get(id=artworkItem.category_id)
        except models.Category.DoesNotExist:
            pass
        return kate.name if kate else None

    def get_author(self, artworkItem):
        artist = None
        try:
            artist = models.Artist.objects.get(id=artworkItem.author_id)
        except models.Artist.DoesNotExist:
            pass
        user = artist.user if artist else None
        return user.email if user else None

    class Meta:
        model = models.Artwork
        fields = ['id', 'name', 'description', 'link', 'category', 'category_name', 'author', 'author_email',
                  'featured', 'favored_by', 'bookmarked_by', 'created_at', 'updated_at']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Favorite
        fields = ['id', 'artwork', 'user']


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bookmark
        fields = ['id', 'artwork', 'user']
