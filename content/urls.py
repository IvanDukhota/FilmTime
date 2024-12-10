# registration/urls.py
from django.urls import path
from .views import Movies, MovieDetailView, ContentViewSet, RecordMovieView, ContentListView, GenreListView, ActorListView,  DirectorListView, ContentContentListView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('movie/', Movies.movie_link, name='movie_link'),
    path('movie/<int:content_id>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/filter/', ContentViewSet.as_view({'get': 'filter_movies'}), name='movie-filter'),
    path("movie/<int:content_id>/record-view/", RecordMovieView.as_view(), name="record_movie_view"),

    path('content-list/', ContentListView.as_view(), name='content-list'),
    path('content-list/content/', ContentContentListView.as_view(), name='content-list-content'),
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('actors/', ActorListView.as_view(), name='actor-list'),
    path('directors/', DirectorListView.as_view(), name='director-list'),
]

