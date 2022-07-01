from django.urls import path, reverse_lazy
from .views import *
app_name = 'tracker'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('filmwatch', FilmWatchListView.as_view(), name='filmwatch_list'),
    path('filmwatch/<int:pk>', FilmWatchDetailView.as_view(), name='filmwatch_detail'),
    path('filmwatch/create', FilmWatchCreateView.as_view(), name='filmwatch_create'),
    path('filmwatch/<int:pk>/update', FilmWatchUpdateView.as_view(), name='filmwatch_update'),
    path('filmwatch/<int:pk>/delete', FilmWatchDeleteView.as_view(success_url=reverse_lazy('tracker:filmwatch_list')), name='filmwatch_delete'),
    path('film', FilmListView.as_view(), name='film_list'),
    path('film/<int:pk>', FilmDetailView.as_view(), name='film_detail'),
    path('film/create', FilmCreateView.as_view(), name='film_create'),
    path('film/<int:pk>/update', FilmUpdateView.as_view(), name='film_update'),
    path('film/<int:pk>/delete', FilmDeleteView.as_view(success_url=reverse_lazy('tracker:film_list')), name='film_delete'),
    path('filmgroup', FilmGroupListView.as_view(), name='filmgroup_list'),
    path('filmgroup/<int:pk>/detail', FilmGroupDetailView.as_view(), name='filmgroup_detail'),
    path('filmgroup/create', FilmGroupCreateView.as_view(), name='filmgroup_create'),
    path('filmgroup/<int:pk>/update', FilmGroupUpdateView.as_view(), name='filmgroup_update'),
    path('filmgroup/<int:pk>/delete', FilmGroupDeleteView.as_view(success_url=reverse_lazy('tracker:filmgroup_list')), name='filmgroup_delete')
]