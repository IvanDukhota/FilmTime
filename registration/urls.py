# registration/urls.py
from django.urls import path
from .views import CustomerListView, CustomerDetailView, CheckUserView

urlpatterns = [
    path('registration-users/', CustomerListView.as_view(), name='userishka-list'),  # Список пользователей
    path('registration-users/<int:id>/', CustomerDetailView.as_view(), name='userishka-detail'),  # Один пользователь
    path('check-user/', CheckUserView.as_view(), name='check-user'),
]