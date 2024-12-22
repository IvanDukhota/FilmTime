from sys import api_version
import stripe
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrModerator
from rest_framework import status, generics, permissions
import time
import hashlib
from django.http import JsonResponse
from django.utils import timezone
from DataBase.models import *
from .serializers import *
from .permissions import IsAdminUser

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json

from django.shortcuts import get_object_or_404
from django.utils.timezone import now

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
    permission_classes = [IsAdminOrModerator]

    def delete(self, request, *args, **kwargs):
        content_id = request.data.get('content_id')
        comment_id = request.data.get('comment_id')

        if content_id is None or comment_id is None:
            return Response({'error': 'content_id и comment_id обязательны.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({'error': 'Контент не найден.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            comment = UserProfileContentInfo.objects.get(id=comment_id, content=content)
        except UserProfileContentInfo.DoesNotExist:
            return Response({'error': 'Комментарий не найден.'}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()

        return Response({'message': 'Комментарий успешно удален.'}, status=status.HTTP_200_OK)

class BanUserView(APIView):
    permission_classes = [IsAdminOrModerator]

    def patch(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        action = request.data.get('action')

        if user_id is None:
            return Response({'error': 'Необходимо указать user_id для изменения статуса.'}, status=status.HTTP_400_BAD_REQUEST)

        if action not in ['ban', 'unban']:
            return Response({'error': 'Неверная операция. Допустимые значения: "ban" или "unban".'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)

        if action == 'ban':
            if user.is_banned:
                return Response({'error': 'Пользователь уже заблокирован.'}, status=status.HTTP_400_BAD_REQUEST)

            user.is_banned = True
            user.save()
            return Response({'message': f'Пользователь {user.email} успешно заблокирован.'}, status=status.HTTP_200_OK)

        if action == 'unban':
            if not user.is_banned:
                return Response({'error': 'Пользователь не заблокирован.'}, status=status.HTTP_400_BAD_REQUEST)

            user.is_banned = False
            user.save()
            return Response({'message': f'Пользователь {user.email} успешно разблокирован.'}, status=status.HTTP_200_OK)


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


def subscription_plans_view(request):
    plans = SubscriptionPlan.objects.all()
    plans_data = [
        {
            "id": plan.id,
            "plan_type": plan.get_plan_type_display(),
            "price_per_month": float(plan.price_per_month),
            "description": plan.description,
            "duration_in_months": plan.duration_in_months,
            "total_price": float(plan.total_price),
        }
        for plan in plans
    ]
    return JsonResponse({"plans": plans_data}, safe=False)



STRIPE_TEST_PUBLIC_KEY = 'pk_test_51QYmu1CdDegJBuD6Ydmvn4KDSC31DZbSxFhAjkygwubSIO00rPy8sszIi3Dz1YJKGhexDsMKoJbrFRDoxJxkEhPY00bUcsa4Aj'
STRIPE_TEST_SECRET_KEY = 'sk_test_51QYmu1CdDegJBuD6fDPBigted2FjHVx8za9ZJL8EW3LuponYBovbvZcQnYG1fFDXylVM3mQqVwkoUBMMnFYu3QgT00QR2n6LJn'


stripe.api_key = STRIPE_TEST_SECRET_KEY


@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000/api/v1/user"
        try:
            data = json.loads(request.body)

            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({'error': 'Authorization token not provided'}, status=401)

            token = auth_header.split(' ')[1]

            from rest_framework_simplejwt.tokens import UntypedToken
            from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
            from rest_framework_simplejwt.authentication import JWTAuthentication

            try:
                UntypedToken(token)
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
            except (InvalidToken, TokenError):
                return JsonResponse({'error': 'Invalid token'}, status=401)

            plan = SubscriptionPlan.objects.get(id=data['plan_id'])

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'uah',
                        'product_data': {
                            'name': plan.plan_type,
                            'description': plan.description
                        },
                        'unit_amount': int(plan.price_per_month * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f"{YOUR_DOMAIN}/success/?token={token}&plan_id={data['plan_id']}",
                cancel_url=f"{YOUR_DOMAIN}/cancel/?token={token}&plan_id={data['plan_id']}",
            )

            return JsonResponse({'url': checkout_session.url})
        except SubscriptionPlan.DoesNotExist:
            return JsonResponse({'error': 'Invalid plan ID'}, status=400)
        except stripe.error.StripeError as e:
            return JsonResponse({'error': f'Stripe Error: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'Unexpected Error: {str(e)}'}, status=500)


from django.http import HttpResponseRedirect

class SuccessView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        plan_id = request.query_params.get('plan_id')
        if not token:
            return Response({"detail": "Token not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        if not plan_id:
            return Response({"detail": "Plan ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from rest_framework_simplejwt.tokens import UntypedToken
            from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
            from rest_framework_simplejwt.authentication import JWTAuthentication

            UntypedToken(token)
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
        except (InvalidToken, TokenError):
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

        subscription_plan = get_object_or_404(SubscriptionPlan, id=plan_id)

        if UserSubscription.objects.filter(user=user, is_active=True).exists():
            return HttpResponseRedirect('http://localhost:3000/views/user_profile.php?status=exists')

        UserSubscription.objects.create(
            user=user,
            plan=subscription_plan,
            purchase_date=now(),
            is_active=True,
        )

        return HttpResponseRedirect('http://localhost:3000/views/user_profile.php?status=success') 

class CancelView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        if not token:
            return Response({"detail": "Token not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            {"detail": "Payment process was canceled."},
            status=status.HTTP_200_OK
        )

from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.timezone import now


class CheckSubscriptionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            subscription = user.user_subscription
            if subscription.is_active and not subscription.is_expired:
                expiration_date = subscription.expiration_date
                remaining_days = (expiration_date - now()).days
                return Response({
                    "has_subscription": True,
                    "remaining_days": remaining_days
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "has_subscription": False,
                    "remaining_days": 0
                }, status=status.HTTP_200_OK)
        except UserSubscription.DoesNotExist:
            return Response({
                "has_subscription": False,
                "remaining_days": 0
            }, status=status.HTTP_200_OK)