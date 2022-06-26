from django.urls import path
from .views import *
urlpatterns = [
    path('', HomeView.as_view()),
    path('<str:table>.json', FilmList.as_view())
]