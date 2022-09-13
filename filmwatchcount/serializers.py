from rest_framework import serializers
from .models import *
class FilmGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmGroup
        exclude = ['User']
class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        exclude = ['User']
class FilmWatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmWatch
        exclude = ['User']
