
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SongViewSet,AlbumViewSet,ArtistVievSet

router = DefaultRouter()
router.register('songs',SongViewSet)
router.register('albums',AlbumViewSet)
router.register('artists',ArtistVievSet)

urlpatterns = [
    path('',include(router.urls))
    # path('album/', AlbumAPIView.as_view(),name = 'album'),
    # path('artist/',ArtistAPIView.as_view(),name = 'artist'),
]