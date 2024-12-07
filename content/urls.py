# registration/urls.py
from django.urls import path
from .views import Movies, MovieDetailView, ContentViewSet
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('movie/', Movies.movie_link, name='movie_link'),
    path('movie/<int:content_id>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/filter/', ContentViewSet.as_view({'get': 'filter_movies'}), name='movie-filter'),
]

