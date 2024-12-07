from django.urls import path
from .views import UserHistoryView, AddToHistoryView

urlpatterns = [
    path('history/', UserHistoryView.as_view(), name='user-history'),
    path('add-history/', AddToHistoryView.as_view(), name='add-to-history'),
]
