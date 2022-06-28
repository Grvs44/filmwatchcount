from django.urls import path, reverse_lazy
from .views import *
app_name = 'tracker'
urlpatterns = [
    path('', FilmWatchListView.as_view(), name='all'),
    path('filmwatch/<int:pk>', FilmWatchDetailView.as_view(), name='filmwatch_detail'),
    path('filmwatch/create', 
        FilmWatchCreateView.as_view(success_url=reverse_lazy('tracker:all')), name='filmwatch_create'),
    path('filmwatch/<int:pk>/update', 
        FilmWatchUpdateView.as_view(success_url=reverse_lazy('tracker:all')), name='filmwatch_update'),
    path('filmwatch/<int:pk>/delete', 
        FilmWatchDeleteView.as_view(success_url=reverse_lazy('tracker:all')), name='filmwatch_delete'),
]