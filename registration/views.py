from django.shortcuts import render
from rest_framework import generics
from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "user_id"


class CheckUserView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            return Response(
                {"exists": True, "username": user.userprofile.username},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)


class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response(
                {"error": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {
                    "error_code": 1001,
                    "error_message": "A user with this email already exists.",
                },
                status=status.HTTP_409_CONFLICT,
            )

        if UserProfile.objects.filter(username=username).exists():
            return Response(
                {
                    "error_code": 1002,
                    "error_message": "A user with this username already exists.",
                },
                status=status.HTTP_409_CONFLICT,
            )

        user = User.objects.create(email=email, role="user")
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user, username=username)

        return Response(
            {"message": "User successfully registered!"}, status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return Response(
                    {"message": "Login successful!"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Incorrect email or password."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except User.DoesNotExist:
            return Response(
                {"error": "Incorrect email or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
