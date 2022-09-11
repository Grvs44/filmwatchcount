from rest_framework import serializers
from .models import *
class FilmGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FilmGroup
        fields = ['id', 'Name']#, 'FilmGroup'
class FilmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'Name', 'ReleaseYear']#, 'FilmGroup'
class FilmWatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FilmWatch
        fields = ['id', 'DateWatched', 'Notes']#, 'Film'