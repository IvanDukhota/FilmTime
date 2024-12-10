from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from DataBase.models import Content, Actor
from .serializers import ContentSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, status
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .serializers import ContentSerializer, ContentListSerializer, ListSerializer, GenreSerializer, ActorSerializer, DirectorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from DataBase.models import UserProfileContentInfo, Content,  ContentList, UserProfile, List, Genre, Actor, Director


class Movies(APIView):
    def movie_link(self, request):
        movie_url = f"http://localhost:8000/media/movies/videoplayback (1).mp4"
        return JsonResponse({'url': movie_url})
    

class MovieDetailView(APIView):
    def get(self, request, content_id):
        try:
            content = Content.objects.get(id=content_id)
            serializer = ContentSerializer(content, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Content.DoesNotExist:
            return Response({"error": "Content not found"}, status=status.HTTP_404_NOT_FOUND)


class ContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    @action(detail=False, methods=['get'])
    def filter_movies(self, request):
        start_year = request.query_params.get('start_year', None)
        end_year = request.query_params.get('end_year', None)
        director = request.query_params.get('director', None)
        actors = request.query_params.getlist('actors', [])
        genres = request.query_params.getlist('genre', [])
        duration = request.query_params.get('duration', None)
        rating = request.query_params.get('rating', None)
        title = request.query_params.get('title', None)

        filters = Q(content_type="movie")

        if start_year and end_year:
            filters &= Q(release_date__year__gte=start_year) & Q(release_date__year__lte=end_year)
        elif start_year:
            filters &= Q(release_date__year__gte=start_year)
        elif end_year:
            filters &= Q(release_date__year__lte=end_year)


        if director:
            filters &= Q(directors__name__icontains=director)


        if actors:
            actor_queries = Q()
            for actor in actors:
                actor_queries |= Q(contentactor__actor__name__icontains=actor)
            filters &= actor_queries

        if genres:
            filters &= Q(contentgenres__genre__name__in=genres)

        if duration:
            filters &= Q(movie__duration__lte=duration)

        if rating:
            filters &= Q(movie__critic_rating__gte=rating)

        if title:
            filters &= Q(title__icontains=title)

        filtered_movies = Content.objects.filter(filters).distinct()
        serializer = self.get_serializer(filtered_movies, many=True)
        return Response(serializer.data)


class RecordMovieView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        content_id = kwargs.get("content_id")
        user_profile = request.user.userprofile

        try:
            content = Content.objects.get(id=content_id)
            record, created = UserProfileContentInfo.objects.get_or_create(
                userprofile=user_profile, content=content
            )
            record.last_watch = now()
            record.save()
            message = "View recorded successfully." if created else "View updated successfully."
            return Response({"message": message}, status=status.HTTP_200_OK)
        except Content.DoesNotExist:
            return Response({"error": "Content not found."}, status=status.HTTP_404_NOT_FOUND)


class ContentListView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):

        list_name = request.data.get('list_name')
        if not list_name:
            return Response({"detail": "List name is required."}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Received list_name: {list_name}")

        userprofile = request.user.userprofile

        existing_list = List.objects.filter(list_name=list_name, userprofile=userprofile).first()
        if existing_list:
            return Response({"detail": "List with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)

        content_list = List.objects.create(userprofile=userprofile, list_name=list_name)

        return Response(ListSerializer(content_list).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        list_id = request.query_params.get('list_id')

        if list_id:
            try:
                content_list = List.objects.get(id=list_id, userprofile=request.user.userprofile)
            except List.DoesNotExist:
                return Response({"detail": "List not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = ListSerializer(content_list, context={'request': request})
        else:
            content_lists = List.objects.filter(userprofile=request.user.userprofile)
            serializer = ListSerializer(content_lists, many=True, context={'request': request})

        return Response(serializer.data)

    def delete(self, request):
        list_id = request.data.get('list_id')

        if not list_id:
            return Response({"detail": "List name is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content_list = List.objects.get(id=list_id, userprofile=request.user.userprofile)
        except List.DoesNotExist:
            return Response({"detail": "List not found."}, status=status.HTTP_404_NOT_FOUND)

        content_list.contents.all().delete()

        content_list.delete()

        return Response({"detail": "List and all its content successfully removed."}, status=status.HTTP_204_NO_CONTENT)


class ContentContentListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        list_id = request.data.get('list_id')
        content_id = request.data.get('content_id')

        if not list_id or not content_id:
            return Response({"detail": "Both list_id and content_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content_list = List.objects.get(id=list_id, userprofile=request.user.userprofile)
        except List.DoesNotExist:
            return Response({"detail": "List not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"detail": "Content not found."}, status=status.HTTP_404_NOT_FOUND)

        content_list_entry, created = ContentList.objects.get_or_create(list=content_list, content=content)

        if created:
            return Response({"detail": "Content successfully added to the list."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Content is already in the list."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        list_id = request.data.get('list_id')
        content_id = request.data.get('content_id')

        if not list_id or not content_id:
            return Response({"detail": "Both list_id and content_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content_list = List.objects.get(id=list_id, userprofile=request.user.userprofile)
        except List.DoesNotExist:
            return Response({"detail": "List not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"detail": "Content not found."}, status=status.HTTP_404_NOT_FOUND)

        content_list_entry = ContentList.objects.filter(list=content_list, content=content).first()

        if not content_list_entry:
            return Response({"detail": "Content not found in the list."}, status=status.HTTP_404_NOT_FOUND)

        content_list_entry.delete()

        return Response({"detail": "Content successfully removed from the list."}, status=status.HTTP_204_NO_CONTENT)


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class ActorListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class DirectorListView(generics.ListAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer