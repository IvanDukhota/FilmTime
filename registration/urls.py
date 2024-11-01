# registration/urls.py
from django.urls import path
from .views import UserListView, UserDetailView, CheckUserView, RegisterUserView, LoginView

urlpatterns = [
    path('registration-users/', UserListView.as_view(), name='userishka-list'),  
    path('registration-users/<int:id>/', UserDetailView.as_view(), name='userishka-detail'), 
    path('check-user/', CheckUserView.as_view(), name='check-user'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]