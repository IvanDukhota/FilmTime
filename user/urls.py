from django.urls import path
from .views import UserHistoryView, AddToHistoryView, SubmitRatingView, GetUserRatingView, GetCommentsView, SubmitCommentView, DeleteCommentView, BanUserView, UserNotificationsView, NotificationDeleteView, UserClearNotificationsView, UserProfileNotificationUpdateView

urlpatterns = [
    path('history/', UserHistoryView.as_view(), name='user-history'),
    path('add-history/', AddToHistoryView.as_view(), name='add-to-history'),
    path('submit-rating/', SubmitRatingView.as_view(), name='submit-rating'),
    path('get-user-rating/', GetUserRatingView.as_view(), name='get-user-rating'),
    path('get-comments/', GetCommentsView.as_view(), name='get-comments'),
    path('submit-comment/', SubmitCommentView.as_view(), name='submit-comment'),
    path('delete-comment/',DeleteCommentView.as_view(), name='delete-comment'),
    path('ban-user/',BanUserView.as_view(),name='ban-user'),
    
    
    path('notifications/user/<int:user_id>/', UserNotificationsView.as_view(), name='user_notifications'),
    path('notifications/<int:id>/', NotificationDeleteView.as_view(), name='delete_notification'),
    path('notifications/user/<int:user_id>/clear/', UserClearNotificationsView.as_view(), name='clear_notifications'),
    path('notifications-upd/<int:pk>/', UserProfileNotificationUpdateView.as_view(), name='update_notification'),

]
