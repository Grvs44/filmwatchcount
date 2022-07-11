from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from .models import *
from .owner import *
from django.urls import reverse
class HomeView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,"tracker/home.html")
class FilmWatchListView(OwnerListView):
    model = FilmWatch
    def get_queryset(self):
        queryset = super().get_queryset()
        if "film" in self.request.GET and self.request.GET["film"].isnumeric(): queryset = queryset.filter(Film_id=int(self.request.GET["film"]))
        if "group" in self.request.GET and self.request.GET["group"].isnumeric(): queryset = queryset.filter(Film__FilmGroup_id=int(self.request.GET["group"]))
        return queryset
class FilmWatchDetailView(OwnerDetailView):
    model = FilmWatch
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["addbtn"] = "add" in self.request.GET
        return context
class FilmWatchCreateView(OwnerCreateView):
    model = FilmWatch
    fields = ["Film","DateWatched","Notes"]
    def get_success_url(self):
        return reverse('tracker:filmwatch_detail',args=[self.object.id]) + "?add"
class FilmWatchUpdateView(OwnerUpdateView):
    model = FilmWatch
    fields = ["Film","DateWatched","Notes"]
    def get_success_url(self):
        return reverse('tracker:filmwatch_detail',args=[self.object.id])
class FilmWatchDuplicateView(OwnerDuplicateView):
    model = FilmWatch
    fields = ["Film","DateWatched","Notes"]
    def get_success_url(self):
        return reverse('tracker:filmwatch_detail',args=[self.object.id]) + "?add"
class FilmWatchDeleteView(OwnerDeleteView):
    model = FilmWatch
class FilmListView(OwnerListView):
    model = Film
    def get_queryset(self):
        if "group" in self.request.GET and self.request.GET["group"].isnumeric(): return super().get_queryset().filter(FilmGroup_id=int(self.request.GET["group"]))
        else: return super().get_queryset()
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
        context["addbtn"] = "add" in self.request.GET
        return context
class FilmCreateView(OwnerCreateView):
    model = Film
    fields = ["FilmGroup","Name","ReleaseYear"]
    def get_success_url(self):
        return reverse('tracker:film_detail',args=[self.object.id]) + "?add"
class FilmUpdateView(OwnerUpdateView):
    model = Film
    fields = ["FilmGroup","Name","ReleaseYear"]
    def get_success_url(self):
        return reverse('tracker:film_detail',args=[self.object.id])
class FilmDuplicateView(OwnerDuplicateView):
    model = Film
    fields = ["FilmGroup","Name","ReleaseYear"]
    def get_success_url(self):
        return reverse('tracker:film_detail',args=[self.object.id]) + "?add"
class FilmDeleteView(OwnerDeleteView):
    model = Film
class FilmCountView(LoginRequiredMixin,View):
    def get(self,request,pk):
        film = get_object_or_404(Film,id=pk)
        if film.User == request.user:
            return HttpResponse(str(FilmWatch.objects.filter(Film=film).count()),content_type="text/plain; charset=utf-8")
        else:
            raise Http404
class FilmGroupListView(OwnerListView):
    model = FilmGroup
    def get_queryset(self):
        if "group" in self.request.GET and self.request.GET["group"].isnumeric(): return super().get_queryset().filter(FilmGroup_id=int(self.request.GET["group"]))
        else: return super().get_queryset()
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
        context["addbtn"] = "add" in self.request.GET
        return context
class FilmGroupCreateView(OwnerCreateView):
    model = FilmGroup
    fields = ["FilmGroup","Name"]
    def get_success_url(self):
        return reverse('tracker:filmgroup_detail',args=[self.object.id]) + "?add"
class FilmGroupUpdateView(OwnerUpdateView):
    model = FilmGroup
    fields = ["FilmGroup","Name"]
    def get_success_url(self):
        return reverse('tracker:filmgroup_detail',args=[self.object.id])
class FilmGroupDuplicateView(OwnerDuplicateView):
    model = FilmGroup
    fields = ["FilmGroup","Name"]
    def get_success_url(self):
        return reverse('tracker:filmgroup_detail',args=[self.object.id]) + "?add"
class FilmGroupDeleteView(OwnerDeleteView):
    model = FilmGroup
class FilmGroupCountView(LoginRequiredMixin,View):
    def get(self,request,pk):
        filmgroup = get_object_or_404(FilmGroup,id=pk)
        if filmgroup.User == request.user:
            return HttpResponse(str(FilmWatch.objects.filter(Film__FilmGroup=filmgroup).count()),content_type="text/plain; charset=utf-8")
        else:
            raise Http404