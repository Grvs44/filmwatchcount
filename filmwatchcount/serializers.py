from rest_framework.serializers import ModelSerializer, CharField
from .models import FilmGroup, Film, FilmWatch
class FilmGroupSerializer(ModelSerializer):
    class Meta:
        model = FilmGroup
        exclude = ['User']
class FilmSerializer(ModelSerializer):
    class Meta:
        model = Film
        exclude = ['User']
class FilmWatchSerializer(ModelSerializer):
    class Meta:
        model = FilmWatch
        exclude = ['User']

class SummarySerializer(ModelSerializer):
    summary = CharField(source='__str__', read_only=True)
    class Meta:
        fields = ['id','summary']
class FilmGroupSummarySerializer(SummarySerializer):
    class Meta(SummarySerializer.Meta):
        model = FilmGroup
class FilmSummarySerializer(SummarySerializer):
    class Meta(SummarySerializer.Meta):
        model = Film
class FilmWatchSummarySerializer(SummarySerializer):
    class Meta(SummarySerializer.Meta):
        model = FilmWatch
