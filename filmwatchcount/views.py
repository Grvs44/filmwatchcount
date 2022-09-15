from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import *
from .pwaviews import *
from .apiviews import *
class HomeView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,"filmwatchcount/home.html")
class SettingsView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'filmwatchcount/settings.html')

class APIListView(View, LoginRequiredMixin):
    api_url = reverse_lazy('filmwatchcount:api-root')
    def get(self,request):
        return render(request,'filmwatchcount/list.html',{'showback':True,'api':self.api_url,'table':self.table})

class FilmWatchView(APIListView):
    table = 'filmwatch'
class FilmView(APIListView):
    table = 'film'
class FilmGroupView(APIListView):
    table = 'filmgroup'
