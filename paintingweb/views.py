from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, logout
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from . import serializers
from . import models


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RegisterSerializer


class LogoutUserAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # serializer_class = serializers.RegisterSerializer

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        logout(request)

        return Response({"success": "Successfully logged out."},
                        status=200)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Artist.objects.all()
    serializer_class = serializers.ArtistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ArtworkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Artwork.objects.all()
    serializer_class = serializers.ArtworkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        art_name = self.request.query_params.get('name') or None
        if art_name:
            queryset = queryset.filter(name__contains=art_name)
        art_author_id = self.request.query_params.get('author_id') or None
        if art_author_id:
            queryset = queryset.filter(author__id__contains=art_author_id)
        art_author_name = self.request.query_params.get('author_name') or None
        if art_author_name:
            queryset = queryset.filter(author__fullname__contains=art_author_name)
        return queryset


class FavoriteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Favorite.objects.all()
    serializer_class = serializers.FavoriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookmarkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Bookmark.objects.all()
    serializer_class = serializers.BookmarkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
