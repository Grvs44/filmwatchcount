from django.core.exceptions import FieldError
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from .serializers import *
from .permissions import *
class TopViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    def get_queryset(self):
        queryset = self.queryset.filter(User=self.request.user)
        if 'order' in self.request.GET:
            try:
                queryset.order_by(self.request.GET['order'])
            except FieldError: pass
        return queryset
    def perform_create(self, serializer):
        serializer.save(User=self.request.user)
    def get_summary_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return self.summary_serializer_class(*args, **kwargs)
    @action(detail=False)
    def summary(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_summary_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_summary_serializer(queryset, many=True)
        return Response(serializer.data)

class FilmGroupViewSet(TopViewSet):
    queryset = FilmGroup.objects.all()
    serializer_class = FilmGroupSerializer
    summary_serializer_class = FilmGroupSummarySerializer
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
    summary_serializer_class = FilmSummarySerializer
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
    summary_serializer_class = FilmWatchSummarySerializer
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
