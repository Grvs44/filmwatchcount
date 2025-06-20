# pylint:disable=no-member
import json

from django.db.models import Count, Max, Min, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from .apiviews import *
from .models import *
from .owner import *


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "filmwatchcount/home.html")


class DeleteRedirectView(LoginRequiredMixin, View):
    viewname = ""

    def get(self, request, pk):
        return render(request, "filmwatchcount/deleteredirect.html", {"pk": pk, "view": self.viewname})


class FilmWatchFields:
    model = FilmWatch
    fields = ["Film", "DateWatched", "Notes"]


class FilmFields:
    model = Film
    fields = ["FilmGroup", "Name", "ReleaseYear"]


class FilmGroupFields:
    model = FilmGroup
    fields = ["FilmGroup", "Name"]


class FilmWatchListView(OwnerListView):
    model = FilmWatch

    def get_queryset(self):
        queryset = super().get_queryset()
        if "film" in self.request.GET and self.request.GET["film"].isnumeric():
            queryset = queryset.filter(Film_id=int(self.request.GET["film"]))
        elif "group" in self.request.GET and self.request.GET["group"].isnumeric():
            if "sub" in self.request.GET:
                filmgroupid = int(self.request.GET["group"])
                ids = FilmGroup.objects.filter(Q(id=filmgroupid) | Q(
                    FilmGroup_id=filmgroupid)).values_list('id', flat=True)
                queryset = queryset.filter(Film__FilmGroup_id__in=ids)
            else:
                queryset = queryset.filter(
                    Film__FilmGroup_id=int(self.request.GET["group"]))
        if 'q' in self.request.GET:
            queryset = queryset.filter(
                Film__Name__icontains=self.request.GET['q'])
        field = self.request.GET.get('sort', None)
        if field:
            queryset = queryset.order_by(field)
        from_date = self.request.GET.get('from', None)
        if from_date:
            queryset = queryset.filter(DateWatched__gte=from_date)
        to_date = self.request.GET.get('to', None)
        if to_date:
            queryset = queryset.filter(DateWatched__lte=to_date)
        return queryset


class FilmWatchDetailView(OwnerDetailView):
    model = FilmWatch


class FilmWatchCreateView(FilmWatchFields, OwnerCreateView):
    def get_success_url(self):
        return reverse('filmwatchcount:filmwatch_detail', args=[self.object.id])


class FilmWatchUpdateView(FilmWatchFields, OwnerUpdateView):
    def get_success_url(self):
        return reverse('filmwatchcount:filmwatch_detail', args=[self.object.id])


class FilmWatchDuplicateView(FilmWatchFields, OwnerDuplicateView):
    def get_success_url(self):
        return reverse('filmwatchcount:filmwatch_detail', args=[self.object.id])


class FilmWatchCreateLinkedView(FilmWatchFields, OwnerDuplicateView):
    def get(self, request, pk, *args, **kwargs):
        self.object = FilmWatch(Film_id=pk)
        return ProcessFormView.get(self, request, *args, **kwargs)

    def get_success_url(self):
        return reverse('filmwatchcount:filmwatch_detail', args=[self.object.id])


class FilmWatchDeleteView(OwnerDeleteView):
    model = FilmWatch

    def get_success_url(self):
        return reverse('filmwatchcount:filmwatch_deleteredirect', args=[self.object.id])


class FilmWatchDeleteRedirectView(DeleteRedirectView):
    viewname = "filmwatch"


class FilmListView(OwnerListView):
    model = Film

    def get_queryset(self):
        queryset = super().get_queryset()
        if "group" in self.request.GET and self.request.GET["group"].isnumeric():
            if "sub" in self.request.GET:
                filmgroupid = int(self.request.GET["group"])
                ids = FilmGroup.objects.filter(Q(id=filmgroupid) | Q(
                    FilmGroup_id=filmgroupid)).values_list('id', flat=True)
                queryset = queryset.filter(FilmGroup_id__in=ids)
            else:
                queryset = queryset.filter(
                    FilmGroup_id=int(self.request.GET["group"]))
        if 'q' in self.request.GET:
            queryset = queryset.filter(Name__icontains=self.request.GET['q'])
        field = self.request.GET.get('sort', None)
        if field:
            if field in ('count', '-count'):
                queryset = queryset.annotate(count=Count('filmwatch'))
            queryset = queryset.order_by(field)
        return queryset


class FilmDetailView(OwnerDetailView):
    model = Film

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filmgrouplist = []
        filmgroup = context["film"].FilmGroup
        while filmgroup is not None:
            filmgrouplist.append(filmgroup)
            filmgroup = filmgroup.FilmGroup
        context["filmgrouplist"] = filmgrouplist
        return context


class FilmCreateView(FilmFields, OwnerCreateView):
    def get_success_url(self):
        return reverse('filmwatchcount:film_detail', args=[self.object.id])


class FilmUpdateView(FilmFields, OwnerUpdateView):
    def get_success_url(self):
        return reverse('filmwatchcount:film_detail', args=[self.object.id])


class FilmDuplicateView(FilmFields, OwnerDuplicateView):
    def get_success_url(self):
        return reverse('filmwatchcount:film_detail', args=[self.object.id])


class FilmCreateLinkedView(FilmFields, OwnerDuplicateView):
    def get(self, request, pk, *args, **kwargs):
        self.object = Film(FilmGroup_id=pk)
        return ProcessFormView.get(self, request, *args, **kwargs)

    def get_success_url(self):
        return reverse('filmwatchcount:film_detail', args=[self.object.id])


class FilmDeleteView(OwnerDeleteView):
    model = Film

    def get_success_url(self):
        return reverse('filmwatchcount:film_deleteredirect', args=[self.object.id])


class FilmDeleteRedirectView(DeleteRedirectView):
    viewname = "film"


class FilmCountView(LoginRequiredMixin, View):
    def get(self, request, pk):
        film = get_object_or_404(Film, id=pk)
        if film.User == request.user:
            return HttpResponse(str(FilmWatch.objects.filter(Film=film).count()), content_type="text/plain; charset=utf-8")
        else:
            raise Http404


class FilmCompareView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "filmwatchcount/filmcompare.html")


class FilmCompareContentView(LoginRequiredMixin, View):
    def get(self, request, films):
        filmlist = json.loads(films)
        filmquery = Film.objects.filter(
            Q(id__in=filmlist) & Q(User=request.user))
        mostwatched = filmquery.annotate(
            watchcount=Count("filmwatch")).order_by("-watchcount")
        mostrecent = filmquery.annotate(lastwatched=Max(
            "filmwatch__DateWatched")).order_by("-lastwatched")
        return render(request, "filmwatchcount/filmcomparecontent.html", {"films": filmquery, "mostwatched": mostwatched, "mostrecent": mostrecent})


class FilmCompareGraphView(LoginRequiredMixin, View):
    def get(self, request, films):
        filmlist = json.loads(films)
        filmquery = Film.objects.filter(
            Q(id__in=filmlist) & Q(User=request.user))
        maxwatch = filmquery.annotate(watchcount=Count(
            "filmwatch")).order_by("-watchcount")[0]
        lastwatch = filmquery.annotate(lastwatched=Max("filmwatch__DateWatched")).order_by(
            "lastwatched").filter(~Q(lastwatched=None))[0].lastwatched
        earliestwatch = filmquery.annotate(firstwatched=Min("filmwatch__DateWatched")).order_by(
            "firstwatched").filter(~Q(firstwatched=None))[0].firstwatched
        latestwatchdelta = (lastwatch - earliestwatch).days
        width = 600
        height = 300
        xscale = width / latestwatchdelta
        yscale = height / maxwatch.watchcount
        filmgraph = []
        for film in filmquery:
            filmwatches = FilmWatch.objects.filter(
                Film=film).filter(~Q(DateWatched=None))
            if len(filmwatches) == 0:
                continue
            points = ""
            xcoord = (filmwatches[0].DateWatched - earliestwatch).days
            ycoord = 1
            points += "%i,%i" % (xcoord, ycoord)
            for i in range(1, len(filmwatches)):
                xcoord = (filmwatches[i].DateWatched - earliestwatch).days
                points += " %i,%i" % (xcoord, ycoord)
                ycoord += 1
                points += " %i,%i" % (xcoord, ycoord)
            xcoord = latestwatchdelta
            points += " %i,%i" % (xcoord, ycoord)
            filmgraph.append([film.Name, points, "black", xcoord, ycoord])
        return render(request, "filmwatchcount/filmcomparegraph.html", {
            "films": filmquery,
            "maxwatch": maxwatch,
            "earliestwatch": earliestwatch,
            "filmgraph": filmgraph,
            "height": height,
            "width": width,
        })


class FilmGroupListView(OwnerListView):
    model = FilmGroup

    def get_queryset(self):
        queryset = super().get_queryset()
        if "group" in self.request.GET and self.request.GET["group"].isnumeric():
            queryset = queryset.filter(
                FilmGroup_id=int(self.request.GET["group"]))
        if 'q' in self.request.GET:
            queryset = queryset.filter(Name__icontains=self.request.GET['q'])
        field = self.request.GET.get('sort', None)
        if field:
            if field.endswith('watch'):
                queryset = queryset.annotate()
            else:
                queryset = queryset.order_by(field)
        return queryset


class FilmGroupDetailView(OwnerDetailView):
    model = FilmGroup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filmgrouplist = []
        filmgroup = context["filmgroup"].FilmGroup
        while filmgroup is not None:
            filmgrouplist.append(filmgroup)
            filmgroup = filmgroup.FilmGroup
        context["filmgrouplist"] = filmgrouplist
        return context


class FilmGroupCreateView(FilmGroupFields, OwnerCreateView):
    def get_success_url(self):
        return reverse('filmwatchcount:filmgroup_detail', args=[self.object.id])


class FilmGroupUpdateView(FilmGroupFields, OwnerUpdateView):
    def get_success_url(self):
        return reverse('filmwatchcount:filmgroup_detail', args=[self.object.id])


class FilmGroupDuplicateView(FilmGroupFields, OwnerDuplicateView):
    def get_success_url(self):
        return reverse('filmwatchcount:filmgroup_detail', args=[self.object.id])


class FilmGroupCreateLinkedView(FilmGroupFields, OwnerDuplicateView):
    def get(self, request, pk, *args, **kwargs):
        self.object = FilmGroup(FilmGroup_id=pk)
        return ProcessFormView.get(self, request, *args, **kwargs)

    def get_success_url(self):
        return reverse('filmwatchcount:filmgroup_detail', args=[self.object.id])


class FilmGroupDeleteView(OwnerDeleteView):
    model = FilmGroup

    def get_success_url(self):
        return reverse('filmwatchcount:filmgroup_deleteredirect', args=[self.object.id])


class FilmGroupDeleteRedirectView(DeleteRedirectView):
    viewname = "filmgroup"


class FilmGroupCountView(LoginRequiredMixin, View):
    def get(self, request, pk):
        filmgroup = get_object_or_404(FilmGroup, id=pk)
        if filmgroup.User == request.user:
            if "sub" in request.GET:
                ids = FilmGroup.objects.filter(Q(id=filmgroup.id) | Q(
                    FilmGroup=filmgroup)).values_list('id', flat=True)
                queryset = FilmWatch.objects.filter(Film__FilmGroup_id__in=ids)
                return HttpResponse(str(queryset.count()), content_type="text/plain; charset=utf-8")
            else:
                return HttpResponse(str(FilmWatch.objects.filter(Film__FilmGroup=filmgroup).count()), content_type="text/plain; charset=utf-8")
        else:
            raise Http404
