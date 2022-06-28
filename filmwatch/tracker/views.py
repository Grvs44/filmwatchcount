from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
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
        else: return HttpResponseNotFound()
        items = table.objects.filter(User=request.user)
        itemlist = []
        for item in items:
            itemlist.append([item.id,str(item)])
        return HttpResponse(json.dumps(itemlist),content_type="application/json")
    def post(self,request,table):
        try:
            if table == "watch":
                if request.POST["select"] == "": filmid = None
                else: filmid = int(request.POST["select"])
                FilmWatch(User=request.user, Film_id=filmid, DateWatched=datetime.strptime(request.POST["date"], "%Y-%m-%d").date(), Notes=request.POST["notes"]).save()
            elif table == "film":
                if request.POST["select"] == "": groupid = None
                else: groupid = int(request.POST["select"])
                Film(User=request.user, FilmGroup_id=groupid, Name=request.POST["film"]).save()
            elif table == "filmgroup":
                FilmGroup(User=request.user, Name=request.POST["name"]).save()
            else:
                return HttpResponseNotFound()
            return HttpResponse()
        except (ValueError,IndexError,TypeError): return HttpResponseBadRequest()
class RemoveFilm(FilmList):
    def post(self,request,table):
        try:
            recordid = int(request.POST["id"])
            if table == "watch":
                get_object_or_404(FilmWatch,pk=recordid).delete()
            elif table == "film":
                get_object_or_404(Film,pk=recordid).delete()
            elif table == "filmgroup":
                get_object_or_404(FilmGroup,pk=recordid).delete()
            else:
                return HttpResponseNotFound()
            if object.User == request.user:
                object.delete()
                return HttpResponse()
            else:
                return HttpResponseForbidden("The requested item cannot be deleted by this user",content_type="text/plain")
        except (ValueError,IndexError,TypeError): return HttpResponseBadRequest()
class UpdateFilm(FilmList):
    def post(self,request,table,id):
        try:
            if table == "watch":
                object = get_object_or_404(FilmWatch,pk=id)
                if request.POST["select"] == "": object.Film_id = None
                else: object.Film_id = int(request.POST["select"])
                object.DateWatched = datetime.strptime(request.POST["date"], "%Y-%m-%d").date()
                object.Notes = request.POST["notes"]
            elif table == "film":
                object = get_object_or_404(Film,pk=id)
                if request.POST["select"] == "": object.FilmGroup_id = None
                else: object.FilmGroup_id = int(request.POST["select"])
                object.Name = request.POST["name"]
            elif table == "filmgroup":
                object = get_object_or_404(FilmGroup,pk=id)
                object.Name = request.POST["name"]
            else:
                return HttpResponseNotFound()
            if object.User == request.user:
                object.save()
                return HttpResponse()
            else:
                return HttpResponseForbidden("The requested item cannot be modified by this user",content_type="text/plain")
        except (ValueError,IndexError,TypeError,KeyError): raise HttpResponseBadRequest()