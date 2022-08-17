from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import logout_then_login
from django.views.generic.base import RedirectView
urlpatterns = [
    path('accounts/logout/?next=<str:login_url>', logout_then_login),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tracker/', include("tracker.urls")),
    path('', RedirectView.as_view(url='/tracker')),
    path('admin/', admin.site.urls)
]