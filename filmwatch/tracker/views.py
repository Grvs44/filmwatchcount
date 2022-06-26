from http.client import HTTPResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from .models import *
import json
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