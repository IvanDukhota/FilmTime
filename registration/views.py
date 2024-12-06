from django.shortcuts import render
from rest_framework import generics, status
from DataBase.models import User, UserProfile
from .serializers import UserSerializer, CustomTokenObtainPairSerializer,  UserProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
import os
from django.http import JsonResponse
import requests
from django.contrib.auth import login
from dotenv import load_dotenv
import http.client
import json
from urllib.parse import urlencode
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import MovieSerializer
from rest_framework.decorators import api_view
from DataBase.models import Content
from .serializers import ContentSerializer
from django.core.files.base import ContentFile
import base64

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
                {"exists": True, "username": user.userprofile.username}, # type: ignore
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

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User successfully registered!",
                "refresh": str(refresh),
                "access": str(refresh.access_token), # type: ignore
            },
            status=status.HTTP_201_CREATED
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
                
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token), # type: ignore
                    },
                    status=status.HTTP_200_OK,
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
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/api/v1/google/callback/"

# URL Google OAuth
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"


def google_login(request):
    google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    redirect_uri = f"{request.build_absolute_uri('/api/v1/google/callback/')}"
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_url = f"{google_auth_url}?{requests.compat.urlencode(params)}" # type: ignore
    return JsonResponse({"auth_url": auth_url})


def google_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Authorization code not provided"}, status=400)

    token_url = "oauth2.googleapis.com"
    token_path = "/token"

    params = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    conn = http.client.HTTPSConnection(token_url)
    conn.request(
        "POST",
        token_path,
        urlencode(params),
        {
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    token_response = conn.getresponse()
    token_data = json.loads(token_response.read().decode())

    if token_response.status == 200 and "access_token" in token_data:
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}

        conn.request("GET", user_info_url, headers=headers)
        user_info_response = conn.getresponse()
        user_info = json.loads(user_info_response.read().decode())

        email = user_info["email"]
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.set_unusable_password()
            user.save()

        login(request, user)

        return JsonResponse(user_info)

    return JsonResponse(
        {"error": "Unable to retrieve access token", "details": token_data}, status=400
    )


FACEBOOK_CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID")
FACEBOOK_CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET")
FACEBOOK_REDIRECT_URI = "http://localhost:8000/api/v1/facebook/callback/"
AUTHORIZATION_BASE_URL = "https://www.facebook.com/v10.0/dialog/oauth"
TOKEN_URL = "https://graph.facebook.com/v10.0/oauth/access_token"


def facebook_login(request):
    params = {
        "client_id": FACEBOOK_CLIENT_ID,
        "redirect_uri": FACEBOOK_REDIRECT_URI,
        "state": "random_state_string",
        "scope": "email,public_profile",
    }
    auth_url = f"{AUTHORIZATION_BASE_URL}?{requests.compat.urlencode(params)}" # type: ignore
    return JsonResponse({"auth_url": auth_url})


def facebook_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Authorization code not provided"}, status=400)

    params = {
        "client_id": FACEBOOK_CLIENT_ID,
        "redirect_uri": FACEBOOK_REDIRECT_URI,
        "client_secret": FACEBOOK_CLIENT_SECRET,
        "code": code,
    }
    token_response = requests.get(TOKEN_URL, params=params)
    token_data = token_response.json()

    if "access_token" in token_data:
        access_token = token_data["access_token"]
        user_info_url = "https://graph.facebook.com/me"
        user_params = {
            "fields": "id,name,email",
            "access_token": access_token,
        }
        user_info_response = requests.get(user_info_url, params=user_params)
        user_info = user_info_response.json()

        print("User Info:", user_info)
        return JsonResponse(user_info)

    print("Error retrieving access token:", token_data)
    return JsonResponse(
        {"error": "Unable to retrieve access token", "details": token_data}, status=400
    )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'This is a protected view!'})


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_profile = user.userprofile

        data = {
            "user_id": user.id,
            "email": user.email,
            "username": user_profile.username,
            "role": user.role,
            "profile_picture": (
                user_profile.profile_picture.url
                if user_profile.profile_picture
                else None
            ),
            "country": user_profile.country,
            "bio": user_profile.bio,
            "status": user_profile.status,
        }

        return Response(data)


class EditUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        user_profile = user.userprofile

        password = request.data.get("password")
        if password:
            user.set_password(password)
            user.save()

        profile_picture = request.FILES.get("profile_picture")
        if profile_picture:
            user_profile.profile_picture = profile_picture

        serializer = UserProfileSerializer(
            user_profile, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Profile updated successfully!"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
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