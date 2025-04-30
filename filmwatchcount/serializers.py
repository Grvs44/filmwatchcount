from rest_framework.serializers import ModelSerializer, CharField
from .models import FilmGroup, Film, FilmWatch
class TopSerializer(ModelSerializer):
    class Meta:
        exclude = ['User']
class FilmGroupSerializer(TopSerializer):
    class Meta(TopSerializer.Meta):
        model = FilmGroup
class FilmSerializer(TopSerializer):
    class Meta(TopSerializer.Meta):
        model = Film
class FilmWatchSerializer(TopSerializer):
    class Meta(TopSerializer.Meta):
        model = FilmWatch

class SummarySerializer(ModelSerializer):
    str = CharField(source='__str__', read_only=True)
    class Meta:
        fields = ['id','str']
class FilmGroupSummarySerializer(SummarySerializer):
    class Meta(SummarySerializer.Meta):
        model = FilmGroup
class FilmSummarySerializer(SummarySerializer):
    class Meta(SummarySerializer.Meta):
        model = Film
class FilmWatchSummarySerializer(SummarySerializer):
    class Meta(SummarySerializer.Meta):
        model = FilmWatch
