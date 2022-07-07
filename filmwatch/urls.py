from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import logout_then_login
urlpatterns = [
    url('', include('pwa.urls')),
    path('', include("tracker.urls")),
    path('accounts/logout/?next=<str:login_url>', logout_then_login),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls)
]