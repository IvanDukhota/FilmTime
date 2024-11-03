from django.shortcuts import render
from rest_framework import generics
from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
import os
from django.http import JsonResponse
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session
import requests
from django.contrib.auth import login
import os
from dotenv import load_dotenv


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


load_dotenv()

# Client configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/api/v1/google/callback/'

# URL Google OAuth
AUTHORIZATION_BASE_URL = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'


def google_login(request):
    google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    redirect_uri = f"{request.build_absolute_uri('/api/v1/google/callback/')}"
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'consent',
    }
    auth_url = f"{google_auth_url}?{requests.compat.urlencode(params)}"
    return JsonResponse({'auth_url': auth_url})


def google_callback(request):
    code = request.GET.get('code')
    token_url = TOKEN_URL

    # Exchange the authorization code for an access token
    params = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }

    token_response = requests.post(token_url, data=params)
    token_data = token_response.json()

    if token_response.status_code == 200 and 'access_token' in token_data:
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {'Authorization': f"Bearer {token_data['access_token']}"}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()

        print("User Info:", user_info)
        return JsonResponse(user_info)

    print("Error retrieving access token:", token_data)
    return JsonResponse({'error': 'Unable to retrieve access token', 'details': token_data}, status=400)
