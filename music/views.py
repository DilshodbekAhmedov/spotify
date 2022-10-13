from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import status
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models.song import Song
from .models.album import Album
from .models.artist import Artist
from rest_framework.viewsets import ModelViewSet

# Create your views here.


# class HelloApiView(APIView):
#
#     def get(self, request):
#         return Response(data={'habar' : "Hello world"})
#
#     def post(self, request):
#         message = f"Hello {request.data['ism']}"
#         return Response(data={"message" : message})
from music.serializers import SongSerializer, AlbumSerializer, ArtistSerializer


# class SongsAPIView(APIView):
#     def get(self, request):
#         song = Song.objects.all()
#         serializer = SongSerializer(song,many=True)
#         return Response(data=serializer.data)
#
#     def post(self, request):
#         serializer = SongSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         song = serializer.save()
#
#         return Response(data=serializer.data)


class SongViewSet(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filter_backends = [filters.OrderingFilter]


    search_fields = ['title','album__artist__name', 'album__title']
    ordering_fields = ["listened", "-listened"]

    def get_queryset(self):
        queryset = Song.objects.all()
        query = self.request.query_params.get('search')

        # if query is not None:
        #     queryset = Song.objects.annotate(
        #         similarity=TrigramSimilarity('title', query)
        #     ).filter(similarity__gt=0.5).order_by('-similarity')

        if query is not None:
            queryset = queryset.filter(title = f"^{query}")

        return queryset

    @action(detail=True, methods=["POST"])
    def listen(self, request, *args, **kwargs):
        song = self.get_object()
        print(song)
        with transaction.atomic():
            song.listened += 1
            song.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"])
    def top(self, request, *args, **kwargs):
        songs = self.get_queryset()
        songs = songs.order_by('-listened')[:5]
        serializer = SongSerializer(songs, many=True)
        return Response(data=serializer.data)


class ArtistVievSet(ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    @action(detail=True, methods=["GET"])
    def albums(self, request, *args, **kwargs):
        artist = self.get_object()
        serializer = AlbumSerializer(artist.album_set.all(), many=True)

        return Response(serializer.data)


class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

# class AlbumAPIView(APIView):
#     def get(self, request):
#         album = Album.objects.all()
#         serializer = AlbumSerializer(album,many=True)
#         return Response(data=serializer.data)
#
# class ArtistAPIView(APIView):
#     def get(self, request):
#         artist = Artist.objects.all()
#         serializer = ArtistSerializer(artist,many=True)
#         return Response(data=serializer.data)
#
#     def post(self, request):
#         serializer = ArtistSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         artist = serializer.save()
#
#         return Response(data=serializer.data)
