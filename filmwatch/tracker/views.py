#from django.shortcuts import render, get_object_or_404
#from django.views import View
#from django.contrib.auth.mixins import LoginRequiredMixin
#from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from .models import *
from .owner import *
#import json
#from datetime import datetime
class FilmWatchListView(OwnerListView):
    model = FilmWatch
class FilmWatchDetailView(OwnerDetailView):
    model = FilmWatch
class FilmWatchCreateView(OwnerCreateView):
    model = FilmWatch
    fields = ["Film","DateWatched","Notes"]
class FilmWatchUpdateView(OwnerUpdateView):
    model = FilmWatch
    fields = ["Film","DateWatched","Notes"]
class FilmWatchDeleteView(OwnerDeleteView):
    model = FilmWatch
class FilmListView(OwnerListView):
    model = Film
class FilmDetailView(OwnerDetailView):
    model = Film
class FilmCreateView(OwnerCreateView):
    model = Film
    fields = ["FilmGroup","Name"]
class FilmUpdateView(OwnerUpdateView):
    model = Film
    fields = ["FilmGroup","Name"]
class FilmDeleteView(OwnerDeleteView):
    model = Film
class FilmGroupListView(OwnerListView):
    model = FilmGroup
class FilmGroupDetailView(OwnerDetailView):
    model = FilmGroup
class FilmGroupCreateView(OwnerCreateView):
    model = FilmGroup
    fields = ["Name"]
class FilmGroupUpdateView(OwnerUpdateView):
    model = FilmGroup
    fields = ["Name"]
class FilmGroupDeleteView(OwnerDeleteView):
    model = FilmGroup