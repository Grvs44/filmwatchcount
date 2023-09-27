from django.urls import path, include

from .views import *

app_name = 'filmwatchcount'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('filmwatch/', FilmWatchView.as_view(), name='filmwatch'),
    path('film/', FilmView.as_view(), name='film'),
    path('filmgroup/', FilmGroupView.as_view(), name='filmgroup'),
    path('settings', SettingsView.as_view(), name='settings'),
]
