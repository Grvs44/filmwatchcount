from rest_framework import viewsets
from .serializers import *
from .permissions import *
class TopViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    def get_queryset(self):
        return self.queryset.filter(User=self.request.user)
class FilmGroupViewSet(TopViewSet):
    queryset = FilmGroup.objects.all()
    serializer_class = FilmGroupSerializer
class FilmViewSet(TopViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
class FilmWatchViewSet(TopViewSet):
    queryset = FilmWatch.objects.all()
    serializer_class = FilmWatchSerializer