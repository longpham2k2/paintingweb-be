from dataclasses import fields
from typing_extensions import Required
from wsgiref.validate import validator
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
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


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'groups']


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
        user = models.User.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        name = ""
        try:
            name = validated_data['name']
        except KeyError as ke:
            pass
        artist = models.Artist.objects.create(
            fullname=name,
            user=user
        )
        artist.save()

        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Artist
        fields = ['id', 'fullname', 'bio',
                  'gender', 'age', 'dateofbirth', 'user']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    background = serializers.SerializerMethodField('featured_artwork', read_only=True)

    def featured_artwork(self, categoryItem):
        return ArtworkSerializer(categoryItem.background()).data
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'background']


class ArtworkSerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        source='category.name', allow_blank=True, allow_null=True)
    author = serializers.CharField(
        source='author.user.email', allow_blank=True, allow_null=True)
    favored_by = serializers.SerializerMethodField('favorite_by')
    bookmarked_by = serializers.SerializerMethodField('bookmark_by')

    def favorite_by(self, artworkItem):
        return FavoriteSerializer(artworkItem.favored_by(), many=True).data

    def bookmark_by(self, artworkItem):
        return BookmarkSerializer(artworkItem.bookmarked_by(), many=True).data

    class Meta:
        model = models.Artwork
        fields = ['id', 'name', 'description', 'link', 'category', 'author',
                  'featured', 'favored_by', 'bookmarked_by', 'created_at', 'updated_at']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Favorite
        fields = ['id', 'artwork', 'user']


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bookmark
        fields = ['id', 'artwork', 'user']
