from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from .models import *
from .owner import *
from .pwaviews import *
from django.urls import reverse
from django.db.models import Q, Max, Count
import json
class HomeView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,"tracker/home.html")
class DeleteRedirectView(LoginRequiredMixin,View):
    viewname = ""
    def get(self,request,pk):
        return render(request,"tracker/deleteredirect.html",{"pk":pk,"view":self.viewname})
class FilmWatchFields:
    model = FilmWatch
    fields = ["Film","DateWatched","Notes"]
class FilmFields:
    model = Film
    fields = ["FilmGroup","Name","ReleaseYear"]
class FilmGroupFields:
    model = FilmGroup
    fields = ["FilmGroup","Name"]
class FilmWatchListView(OwnerListView):
    model = FilmWatch
    def get_queryset(self):
        queryset = super().get_queryset()
        if "film" in self.request.GET and self.request.GET["film"].isnumeric(): queryset = queryset.filter(Film_id=int(self.request.GET["film"]))
        elif "group" in self.request.GET and self.request.GET["group"].isnumeric():
            if "sub" in self.request.GET:
                filmgroupid = int(self.request.GET["group"])
                ids = FilmGroup.objects.filter(Q(id=filmgroupid)|Q(FilmGroup_id=filmgroupid)).values_list('id',flat=True)
                queryset = queryset.filter(Film__FilmGroup_id__in=ids)
            else: queryset = queryset.filter(Film__FilmGroup_id=int(self.request.GET["group"]))
        return queryset
class FilmWatchDetailView(OwnerDetailView):
    model = FilmWatch
class FilmWatchCreateView(FilmWatchFields,OwnerCreateView):
    def get_success_url(self):
        return reverse('tracker:filmwatch_detail',args=[self.object.id])
class FilmWatchUpdateView(FilmWatchFields,OwnerUpdateView):
    def get_success_url(self):
        return reverse('tracker:filmwatch_detail',args=[self.object.id])
class FilmWatchDuplicateView(FilmWatchFields,OwnerDuplicateView):
    def get_success_url(self):
        return reverse('tracker:filmwatch_detail',args=[self.object.id])
class FilmWatchCreateLinkedView(FilmWatchFields,OwnerDuplicateView):
    def get(self,request,pk,*args,**kwargs):
        self.object = FilmWatch(Film_id=pk)
        return ProcessFormView.get(self,request,*args,**kwargs)
class FilmWatchDeleteView(OwnerDeleteView):
    model = FilmWatch
    def get_success_url(self):
        return reverse('tracker:filmwatch_deleteredirect',args=[self.object.id])
class FilmWatchDeleteRedirectView(DeleteRedirectView):
    viewname = "filmwatch"
class FilmListView(OwnerListView):
    model = Film
    def get_queryset(self):
        queryset = super().get_queryset()
        if "group" in self.request.GET and self.request.GET["group"].isnumeric():
            if "sub" in self.request.GET:
                filmgroupid = int(self.request.GET["group"])
                ids = FilmGroup.objects.filter(Q(id=filmgroupid)|Q(FilmGroup_id=filmgroupid)).values_list('id',flat=True)
                queryset = queryset.filter(FilmGroup_id__in=ids)
            else: queryset = queryset.filter(FilmGroup_id=int(self.request.GET["group"]))
        return queryset
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
class FilmCreateView(FilmFields,OwnerCreateView):
    def get_success_url(self):
        return reverse('tracker:film_detail',args=[self.object.id])
class FilmUpdateView(FilmFields,OwnerUpdateView):
    def get_success_url(self):
        return reverse('tracker:film_detail',args=[self.object.id])
class FilmDuplicateView(FilmFields,OwnerDuplicateView):
    def get_success_url(self):
        return reverse('tracker:film_detail',args=[self.object.id])
class FilmCreateLinkedView(FilmFields,OwnerDuplicateView):
    def get(self,request,pk,*args,**kwargs):
        self.object = Film(FilmGroup_id=pk)
        return ProcessFormView.get(self,request,*args,**kwargs)
class FilmDeleteView(OwnerDeleteView):
    model = Film
    def get_success_url(self):
        return reverse('tracker:film_deleteredirect',args=[self.object.id])
class FilmDeleteRedirectView(DeleteRedirectView):
    viewname = "film"
class FilmCountView(LoginRequiredMixin,View):
    def get(self,request,pk):
        film = get_object_or_404(Film,id=pk)
        if film.User == request.user:
            return HttpResponse(str(FilmWatch.objects.filter(Film=film).count()),content_type="text/plain; charset=utf-8")
        else:
            raise Http404
class FilmCompareView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,"tracker/filmcompare.html")
class FilmCompareContentView(LoginRequiredMixin,View):
    def get(self,request,films):
        filmlist = json.loads(films)
        filmquery = Film.objects.filter(Q(id__in=filmlist)&Q(User=request.user))
        mostwatched = filmquery.annotate(watchcount=Count("filmwatch")).order_by("-watchcount")
        mostrecent = filmquery.annotate(lastwatched=Max("filmwatch__DateWatched")).order_by("-lastwatched")
        return render(request,"tracker/filmcomparecontent.html",{"films":filmquery,"mostwatched":mostwatched,"mostrecent":mostrecent})
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
        return context
class FilmGroupCreateView(FilmGroupFields,OwnerCreateView):
    def get_success_url(self):
        return reverse('tracker:filmgroup_detail',args=[self.object.id])
class FilmGroupUpdateView(FilmGroupFields,OwnerUpdateView):
    def get_success_url(self):
        return reverse('tracker:filmgroup_detail',args=[self.object.id])
class FilmGroupDuplicateView(FilmGroupFields,OwnerDuplicateView):
    def get_success_url(self):
        return reverse('tracker:filmgroup_detail',args=[self.object.id])
class FilmGroupCreateLinkedView(FilmGroupFields,OwnerDuplicateView):
    def get(self,request,pk,*args,**kwargs):
        self.object = FilmGroup(FilmGroup_id=pk)
        return ProcessFormView.get(self,request,*args,**kwargs)
class FilmGroupDeleteView(OwnerDeleteView):
    model = FilmGroup
    def get_success_url(self):
        return reverse('tracker:filmgroup_deleteredirect',args=[self.object.id])
class FilmGroupDeleteRedirectView(DeleteRedirectView):
    viewname = "filmgroup"
class FilmGroupCountView(LoginRequiredMixin,View):
    def get(self,request,pk):
        filmgroup = get_object_or_404(FilmGroup,id=pk)
        if filmgroup.User == request.user:
            return HttpResponse(str(FilmWatch.objects.filter(Film__FilmGroup=filmgroup).count()),content_type="text/plain; charset=utf-8")
        else:
            raise Http404
class SettingsView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'tracker/settings.html')