from rest_framework import serializers
from music.models import song,album,artist
from rest_framework.exceptions import ValidationError

class ArtistSerializer(serializers.ModelSerializer):


    class Meta:
        model = artist.Artist
        fields = '__all__'
    def validate_picture(self, value):
        print(value)
        if not value.startswith("https"):
            raise ValidationError(detail="http emas https bo'lishi kerak")
        return value

class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    class Meta:
        model = album.Album
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    album = AlbumSerializer()
    class Meta:
        model = song.Song
        fields = ('id','title','album','cover','source','listened')

    def validate_source(self, value):

        if not value.endswith(".mp3"):
            raise ValidationError(detail='mp3 file is required')

        return value

