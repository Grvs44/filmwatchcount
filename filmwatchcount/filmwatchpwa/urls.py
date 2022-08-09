from django.urls import path
from .views import *
app_name = 'filmwatchpwa'
urlpatterns = [
    path('pwadate',date_list,name='pwadate'),
    path('manifest.webmanifest',manifest,name='manifest'),
    path('pwabuilder-sw.js',serviceworker),
    path('sw_register.js',serviceworker_register,name="swregister"),
    path('offline.html',offline)
]