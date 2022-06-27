from http.client import HTTPResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from .models import *
import json
from datetime import datetime
class HomeView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,"tracker/home.html")
class FilmList(LoginRequiredMixin,View):
    def get(self,request,table):
        if table == "watch": table = FilmWatch
        elif table == "film": table = Film
        elif table == "group": table = FilmGroup
        else: raise Http404
        items = table.objects.filter(User=request.user)
        itemlist = []
        for item in items:
            itemlist.append([item.id,str(item)])
        return HttpResponse(json.dumps(itemlist),content_type="application/json")
    def post(self,request,table):
        try:
            if table == "watch":
                FilmWatch(User=request.user, Film_id=int(request.POST["select"]), DateWatched=datetime.strptime(request.POST["date"], "%Y-%m-%d").date(), Notes=request.POST["notes"]).save()
            elif table == "film":
                groupid = int(request.POST["select"])
                if groupid == -1: groupid = None
                Film(User=request.user, FilmGroup_id=groupid, Name=request.POST["film"]).save()
            elif table == "filmgroup":
                FilmGroup(User=request.user, Name=request.POST["name"]).save()
            else:
                raise Http404
            return HttpResponse()
        except (ValueError,IndexError,TypeError): raise HttpResponseBadRequest()