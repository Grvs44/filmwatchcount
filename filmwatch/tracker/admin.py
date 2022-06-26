from django.contrib import admin
from .models import *
admin.site.register(FilmGroup)
admin.site.register(Film)
admin.site.register(FilmWatch)