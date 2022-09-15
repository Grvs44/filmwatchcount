from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
app_name = 'filmwatchcount'
router = DefaultRouter()
router.register(r'filmgroup', FilmGroupViewSet)
router.register(r'film', FilmViewSet)
router.register(r'filmwatch', FilmWatchViewSet)
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/', include(router.urls)),
    path('filmwatch/', FilmWatchView.as_view(), name='filmwatch'),
    path('film/', FilmView.as_view(), name='film'),
    path('filmgroup/', FilmGroupView.as_view(), name='filmgroup'),
    #path('filmcompare', FilmCompareView.as_view(), name='filmcompare'),
    #path('filmcompare<str:films>', FilmCompareContentView.as_view(), name='filmcomparecontent'),
    #path('filmcompare<str:films>/graph', FilmCompareGraphView.as_view(), name='filmcomparegraph'),
    path('settings', SettingsView.as_view(), name='settings'),
    path('pwadate',date_list,name='pwadate'),
    path('manifest.webmanifest',manifest,name='manifest'),
    path('pwabuilder-sw.js',serviceworker,name='sw'),
    path('sw_register.js',serviceworker_register,name="swregister"),
    path('offline.html',offline,name='offline'),
]