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
from .serializers import ContentSerializer, ContentListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from DataBase.models import UserProfileContentInfo, Content,  ContentList, UserProfile

class Movies(APIView):
    def movie_link(self, request):
        movie_url = f"http://localhost:8000/media/movies/videoplayback (1).mp4"
        return JsonResponse({'url': movie_url})
    

class MovieDetailView(APIView):
    def get(self, request, content_id):
        try:
            content = Content.objects.get(id=content_id)
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

    def get(self, request):
        list_name = request.query_params.get('list_name')
        if list_name:
            content_lists = ContentList.objects.filter(list_name=list_name, userprofile=request.user.userprofile)
        else:
            content_lists = ContentList.objects.filter(userprofile=request.user.userprofile)

        serializer = ContentListSerializer(content_lists, many=True)
        return Response(serializer.data)

    def post(self, request):
        content_id = request.data.get('content_id')
        list_name = request.data.get('list_name')

        if not content_id or not list_name:
            return Response({"detail": "Content ID and List Name are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"detail": "Content not found."}, status=status.HTTP_404_NOT_FOUND)

        userprofile = request.user.userprofile

        existing_content = ContentList.objects.filter(
            content=content,
            list_name=list_name,
            userprofile=userprofile
        ).exists()

        if existing_content:
            return Response({"detail": "This content is already in the specified list."}, status=status.HTTP_400_BAD_REQUEST)

        content_list = ContentList.objects.create(
            userprofile=userprofile,
            content=content,
            list_name=list_name
        )

        return Response(ContentListSerializer(content_list).data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        content_id = request.data.get('content_id')
        list_name = request.data.get('list_name')

        if not content_id and list_name:
            return self.delete_all(list_name=list_name,userprofile=request.user.userprofile)


        if not content_id or not list_name:
            return Response({"detail": "Content ID and List Name are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"detail": "Content not found."}, status=status.HTTP_404_NOT_FOUND)

        userprofile = request.user.userprofile

        content_list = ContentList.objects.filter(
            content=content,
            list_name=list_name,
            userprofile=userprofile
        ).first()

        if not content_list:
            return Response({"detail": "Content not found in the specified list."}, status=status.HTTP_404_NOT_FOUND)

        content_list.delete()

        return Response({"detail": "Content successfully removed from the list."}, status=status.HTTP_204_NO_CONTENT)

    def delete_all(self, list_name, userprofile):


        if not list_name:
            return Response({"detail": "List Name is required."}, status=status.HTTP_400_BAD_REQUEST)


        content_lists = ContentList.objects.filter(list_name=list_name, userprofile=userprofile)

        if not content_lists.exists():
            return Response({"detail": "No content found in the specified list."}, status=status.HTTP_404_NOT_FOUND)

        content_lists.delete()

        return Response({"detail": "All content successfully removed from the list."}, status=status.HTTP_204_NO_CONTENT)
