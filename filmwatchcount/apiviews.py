from django.core.exceptions import FieldError
from rest_framework import viewsets
from .serializers import *
from .permissions import *
class TopViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    def get_queryset(self):
        print(self.request.GET)
        queryset = self.queryset.filter(User=self.request.user)
        if 'order' in self.request.GET:
            try:
                queryset.order_by(self.request.GET['order'])
            except FieldError: pass
        return queryset
    def perform_create(self, serializer):
        serializer.save(User=self.request.user)

class FilmGroupViewSet(TopViewSet):
    queryset = FilmGroup.objects.all()
    serializer_class = FilmGroupSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'group' in self.request.GET and self.request.GET['group'].isnumeric():
            filmgroupid = int(self.request.GET['group'])
            if 'sub' in self.request.GET:
                ids = FilmGroup.objects.filter(Q(id=filmgroupid)|Q(FilmGroup_id=filmgroupid)).values_list('id',flat=True)
                queryset = queryset.filter(FilmGroup_id__in=ids)
            else:
                queryset = queryset.filter(FilmGroup_id=filmgroupid)
        return queryset

class FilmViewSet(TopViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        if "group" in self.request.GET and self.request.GET["group"].isnumeric():
            if "sub" in self.request.GET:
                filmgroupid = int(self.request.GET["group"])
                ids = FilmGroup.objects.filter(Q(id=filmgroupid)|Q(FilmGroup_id=filmgroupid)).values_list('id',flat=True)
                queryset = queryset.filter(FilmGroup_id__in=ids)
            else: queryset = queryset.filter(FilmGroup_id=int(self.request.GET["group"]))
        return queryset

class FilmWatchViewSet(TopViewSet):
    queryset = FilmWatch.objects.all()
    serializer_class = FilmWatchSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        if "film" in self.request.GET and self.request.GET["film"].isnumeric():
            queryset = queryset.filter(Film_id=int(self.request.GET["film"]))
        elif "group" in self.request.GET and self.request.GET["group"].isnumeric():
            if "sub" in self.request.GET:
                filmgroupid = int(self.request.GET["group"])
                ids = FilmGroup.objects.filter(Q(id=filmgroupid)|Q(FilmGroup_id=filmgroupid)).values_list('id',flat=True)
                queryset = queryset.filter(Film__FilmGroup_id__in=ids)
            else: queryset = queryset.filter(Film__FilmGroup_id=int(self.request.GET["group"]))
        return queryset
