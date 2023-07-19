from django.urls import include, path
from rest_framework import routers
from paintingweb import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'artists', views.ArtistViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'artworks', views.ArtworkViewSet)
router.register(r'favorites', views.FavoriteViewSet)
router.register(r'bookmarks', views.BookmarkViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api/login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/register/', views.RegisterUserAPIView.as_view(), name='register'),
    path('api/token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', views.LogoutUserAPIView.as_view(), name='logout'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
