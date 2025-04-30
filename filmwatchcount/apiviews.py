from django.core.exceptions import FieldError
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from .permissions import *
from .metadata import TextMetadata
from . import filters
class TopViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    authentication_classes = [SessionAuthentication]
    filter_backends = [filters.OwnerFilter,SearchFilter,DjangoFilterBackend,OrderingFilter]
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
    search_fields = ['Name']
    ordering_fields = ['Name']
    filterset_fields = ['FilmGroup']

class FilmViewSet(TopViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    summary_serializer_class = FilmSummarySerializer
    search_fields = ['Name']
    ordering_fields = ['Name','ReleaseYear']
    filterset_fields = {
        'FilmGroup':['exact'],
        'ReleaseYear': ['exact','lt','gt'],
    }

class FilmWatchViewSet(TopViewSet):
    queryset = FilmWatch.objects.all()
    serializer_class = FilmWatchSerializer
    summary_serializer_class = FilmWatchSummarySerializer
    metadata_class = TextMetadata
    ordering_fields = ['DateWatched']
    filterset_fields = {
        'Film': ['exact'],
        'DateWatched': ['exact','lt','gt'],
    }
