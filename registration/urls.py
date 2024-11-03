# registration/urls.py
from django.urls import path
from .views import UserListView, UserDetailView, CheckUserView, RegisterUserView, LoginView,  google_login,google_callback, facebook_login, facebook_callback

urlpatterns = [
    path('registration-users/', UserListView.as_view(), name='userishka-list'),  
    path('registration-users/<int:id>/', UserDetailView.as_view(), name='userishka-detail'), 
    path('check-user/', CheckUserView.as_view(), name='check-user'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('facebook/login/', facebook_login, name='facebook-login'),
    path('facebook/callback/', facebook_callback, name='facebook-callback'),
]