from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from DataBase.models import Content, Actor
from .serializers import ContentSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, status

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .serializers import ContentSerializer


class Movies(APIView):
    def movie_link(self, request):
        movie_url = f"http://localhost:8000/media/movies/videoplayback (1).mp4"
        return JsonResponse({'url': movie_url})
    

class MovieDetailView(APIView):
    def get(self, request, content_id):
        try:
            content = Content.objects.get(content_id=content_id)
            serializer = ContentSerializer(content)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Content.DoesNotExist:
            return Response({"error": "Content not found"}, status=status.HTTP_404_NOT_FOUND)
        

class ContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    @action(detail=False, methods=['get'])
    def filter_movies(self, request):
        release_date = request.query_params.get('release_date', None)
        director = request.query_params.get('director', None)
        actors = request.query_params.getlist('actor', [])
        duration = request.query_params.get('duration', None)
        rating = request.query_params.get('rating', None)
        title = request.query_params.get('title', None)

        filters = Q(content_type="movie")
        if release_date:
            filters &= Q(release_date=release_date)

        if director:
            filters &= Q(directors__name__icontains=director)

        if actors:
            filters &= Q(actors__name__in=actors)

        if duration:
            filters &= Q(movie__duration__lte=duration)

        if rating:
            filters &= Q(rating__gte=rating)

        if title:
            filters &= Q(title__icontains=title)

        filtered_movies = Content.objects.filter(filters).distinct()

        serializer = self.get_serializer(filtered_movies, many=True)

        return Response(serializer.data)

