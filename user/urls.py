from django.urls import path
from .views import UserHistoryView, AddToHistoryView, SubmitRatingView, GetUserRatingView, GetCommentsView, SubmitCommentView, DeleteCommentView, BanUserView, AllNotificationsView, UserNotificationsView

urlpatterns = [
    path('history/', UserHistoryView.as_view(), name='user-history'),
    path('add-history/', AddToHistoryView.as_view(), name='add-to-history'),
    path('submit-rating/', SubmitRatingView.as_view(), name='submit-rating'),
    path('get-user-rating/', GetUserRatingView.as_view(), name='get-user-rating'),
    path('get-comments/', GetCommentsView.as_view(), name='get-comments'),
    path('submit-comment/', SubmitCommentView.as_view(), name='submit-comment'),
    path('delete-comment/',DeleteCommentView.as_view(), name='delete-comment'),
    path('ban-user/',BanUserView.as_view(),name='ban-user'),
    path('notifications/', AllNotificationsView.as_view(), name='all-notifications'),
    path('notifications/user/<int:user_id>/', UserNotificationsView.as_view(), name='user-notifications'),
]
