from django.urls import path
from .views import *
app_name = 'filmwatchpwa'
urlpatterns = [
    path('manifest.json',manifest),
    path('pwabuilder-sw.js',serviceworker),
    path('pwabuilder-sw-update.js',serviceworker_update),
    path('offline.html',offline)
]