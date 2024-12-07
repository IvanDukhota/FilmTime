# registration/urls.py
from django.urls import path
from .views import Movies, MovieDetailView, ContentViewSet, RecordMovieView, ContentListView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('movie/', Movies.movie_link, name='movie_link'),
    path('movie/<int:content_id>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/filter/', ContentViewSet.as_view({'get': 'filter_movies'}), name='movie-filter'),
    path("movie/<int:content_id>/record-view/", RecordMovieView.as_view(), name="record_movie_view"),

    path('content-list/', ContentListView.as_view(), name='content-list'),
]

