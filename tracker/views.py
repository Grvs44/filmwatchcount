from django.shortcuts import render
from django.views import View
from .models import *
from .owner import *
from django.urls import reverse
class HomeView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,"tracker/home.html")
class FilmWatchListView(OwnerListView):
    model = FilmWatch
class FilmWatchDetailView(OwnerDetailView):
    model = FilmWatch
class FilmWatchCreateView(OwnerCreateView):
    model = FilmWatch
    fields = ["Film","DateWatched","Notes"]
    def get_success_url(self):
        return reverse('tracker:filmwatch_detail',args=[self.object.id])
class FilmWatchUpdateView(OwnerUpdateView):
    model = FilmWatch
    fields = ["Film","DateWatched","Notes"]
    def get_success_url(self):
        return reverse('tracker:filmwatch_detail',args=[self.object.id])
class FilmWatchDeleteView(OwnerDeleteView):
    model = FilmWatch
class FilmListView(OwnerListView):
    model = Film
class FilmDetailView(OwnerDetailView):
    model = Film
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filmgrouplist = []
        filmgroup = context["film"].FilmGroup
        while filmgroup != None:
            filmgrouplist.append(filmgroup)
            filmgroup = filmgroup.FilmGroup
        context["filmgrouplist"] = filmgrouplist
        return context
class FilmCreateView(OwnerCreateView):
    model = Film
    fields = ["FilmGroup","Name"]
    def get_success_url(self):
        return reverse('tracker:film_detail',args=[self.object.id])
class FilmUpdateView(OwnerUpdateView):
    model = Film
    fields = ["FilmGroup","Name"]
    def get_success_url(self):
        return reverse('tracker:film_detail',args=[self.object.id])
class FilmDeleteView(OwnerDeleteView):
    model = Film
class FilmGroupListView(OwnerListView):
    model = FilmGroup
class FilmGroupDetailView(OwnerDetailView):
    model = FilmGroup
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filmgrouplist = []
        filmgroup = context["filmgroup"].FilmGroup
        while filmgroup != None:
            filmgrouplist.append(filmgroup)
            filmgroup = filmgroup.FilmGroup
        context["filmgrouplist"] = filmgrouplist
        return context
class FilmGroupCreateView(OwnerCreateView):
    model = FilmGroup
    fields = ["FilmGroup","Name"]
    def get_success_url(self):
        return reverse('tracker:filmgroup_detail',args=[self.object.id])
class FilmGroupUpdateView(OwnerUpdateView):
    model = FilmGroup
    fields = ["FilmGroup","Name"]
    def get_success_url(self):
        return reverse('tracker:filmgroup_detail',args=[self.object.id])
class FilmGroupDeleteView(OwnerDeleteView):
    model = FilmGroup