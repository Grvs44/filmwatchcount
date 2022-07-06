from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import logout_then_login
from django.views.generic.base import RedirectView
urlpatterns = [
    path('', include("tracker.urls")),
    path('/manifest.json', RedirectView.as_view(url="/static/manifest.json")),
    path('/pwabuilder-sw.js', RedirectView.as_view(url="/static/pwabuilder-sw.js")),
    path('/pwabuilder-sw-register.js', RedirectView.as_view(url="pwabuilder-sw-register.js")),
    path('accounts/logout/?next=<str:login_url>', logout_then_login),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls)
]