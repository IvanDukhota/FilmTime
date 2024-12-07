from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone  
from DataBase.models import UserProfileContentInfo, Content  
from .serializers import UserHistorySerializer  


class UserHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile
        history = UserProfileContentInfo.objects.filter(userprofile=user_profile).select_related('content')

  
        serializer = UserHistorySerializer(history, many=True)
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

