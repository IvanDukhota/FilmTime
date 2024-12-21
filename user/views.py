from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, permissions
from django.utils import timezone
from DataBase.models import *
from .serializers import *
from .permissions import IsAdminUser


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
            return (UserProfileContentInfo.objects
                    .filter(content__id=content_id, comment__isnull=False)
                    .select_related('content', 'userprofile')
                    .order_by('-comment_date'))
        return UserProfileContentInfo.objects.none()


class DeleteCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        content_id = request.data.get('content_id')
        comment_id = request.data.get('comment_id')

        if content_id is None or comment_id is None:
            return Response({'error': 'content_id и comment_id обязательны.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({'error': 'Content не найден.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user_content_info = UserProfileContentInfo.objects.get(id=comment_id, content=content)
        except UserProfileContentInfo.DoesNotExist:
            return Response({'error': 'Комментарий не найден.'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.role in ['moderator', 'admin']:
            return Response({'error': 'Недостаточно прав для удаления комментария.'}, status=status.HTTP_403_FORBIDDEN)

        user_content_info.delete()

        return Response({'message': 'Комментарий успешно удален.'}, status=status.HTTP_200_OK)


class BanUserView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = None

    def patch(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        action = request.data.get('action')

        if user_id is None:
            return Response({'error': 'Необхідно вказати user_id для зміни статусу.'}, status=status.HTTP_400_BAD_REQUEST)

        if action not in ['ban', 'unban']:
            return Response({'error': 'Невірна дія. Дозволені значення: "ban" або "unban".'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Користувач не знайдений.'}, status=status.HTTP_404_NOT_FOUND)

        if action == 'ban':
            if user.is_banned:
                return Response({'error': 'Користувач вже заблокований.'}, status=status.HTTP_400_BAD_REQUEST)

            user.is_banned = True
            user.save()
            return Response({'message': f'Користувач {user.email} забанений успішно.'}, status=status.HTTP_200_OK)

        if action == 'unban':
            if not user.is_banned:
                return Response({'error': 'Користувач не заблокований.'}, status=status.HTTP_400_BAD_REQUEST)

            user.is_banned = False
            user.save()
            return Response({'message': f'Користувач {user.email} розбанений успішно.'}, status=status.HTTP_200_OK)





    


class UserNotificationsView(generics.ListAPIView):
    serializer_class = UserProfileNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return UserProfileNotifications.objects.filter(userprofile__user__id=user_id).order_by('-notification__datetime')

class NotificationDeleteView(generics.DestroyAPIView):
    queryset = UserProfileNotifications.objects.all()
    serializer_class = UserProfileNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.userprofile.user != request.user:
            return Response({"detail": "Не дозволено."}, status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)

class UserClearNotificationsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        if request.user.id != int(user_id):
            return Response({"detail": "Не дозволено."}, status=status.HTTP_403_FORBIDDEN)
        deleted, _ = UserProfileNotifications.objects.filter(userprofile__user__id=user_id).delete()
        return Response({"deleted": deleted}, status=status.HTTP_204_NO_CONTENT)
    

class UserProfileNotificationUpdateView(generics.UpdateAPIView):
    queryset = UserProfileNotifications.objects.all()
    serializer_class = UserProfileNotificationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfileNotifications.objects.filter(userprofile=self.request.user.userprofile)