from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, permissions
from django.utils import timezone  
from DataBase.models import UserProfileContentInfo, Content  
from .serializers import UserHistorySerializer


class UserHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile
        history = UserProfileContentInfo.objects.filter(userprofile=user_profile).select_related('content')

        serializer = UserHistorySerializer(history, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class AddToHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_profile = request.user.userprofile
        content_id = request.data.get("content_id")

        if not content_id:
            return Response({"error": "Content ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"error": "Content not found"}, status=status.HTTP_404_NOT_FOUND)

    
        history_entry, created = UserProfileContentInfo.objects.update_or_create(
            userprofile=user_profile,
            content=content,
            defaults={
                "last_watch": timezone.now(),
            },
        )

        return Response(
            {"message": "Content added to history", "created": created},
            status=status.HTTP_201_CREATED,
        )



class SubmitRatingView(generics.CreateAPIView):
    serializer_class = UserHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        rating = request.data.get('user_rating')
        content_id = request.data.get('content_id')

        if rating is None or content_id is None:
            return Response({'error': 'user_rating и content_id обязательны.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({'error': 'Content не найден.'}, status=status.HTTP_404_NOT_FOUND)

        userprofile = request.user.userprofile

        user_content_info, created = UserProfileContentInfo.objects.get_or_create(
            userprofile=userprofile,
            content=content,
            defaults={'user_rating': rating}
        )

        if not created:
            user_content_info.user_rating = rating
            user_content_info.save()

        serializer = self.get_serializer(user_content_info)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetUserRatingView(generics.RetrieveAPIView):
    serializer_class = UserHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        content_id = request.query_params.get('content_id')
        if not content_id:
            return Response({'error': 'content_id обязателен.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({'error': 'Content не найден.'}, status=status.HTTP_404_NOT_FOUND)

        userprofile = request.user.userprofile

        try:
            user_content_info = UserProfileContentInfo.objects.get(userprofile=userprofile, content=content)
            serializer = self.get_serializer(user_content_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfileContentInfo.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        

class SubmitCommentView(generics.UpdateAPIView):
    serializer_class = UserHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        content_id = request.data.get('content_id')
        comment_text = request.data.get('comment')
        
        if content_id is None or comment_text is None:
            return Response({'error': 'content_id и comment обязательны.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({'error': 'Content не найден.'}, status=status.HTTP_404_NOT_FOUND)
        
        userprofile = request.user.userprofile
        
        user_content_info, created = UserProfileContentInfo.objects.get_or_create(
            userprofile=userprofile,
            content=content,
            defaults={'comment': comment_text}
        )
        
        if not created:
            user_content_info.comment = comment_text
            user_content_info.save()
        
        serializer = self.get_serializer(user_content_info)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetCommentsView(generics.ListAPIView):
    serializer_class = UserHistorySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        content_id = self.request.query_params.get('content_id')
        if content_id:
            return UserProfileContentInfo.objects.filter(content__id=content_id, comment__isnull=False).order_by('-comment_date')
        return UserProfileContentInfo.objects.none()