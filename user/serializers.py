from rest_framework import serializers
from DataBase.models import *

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'plan_type', 'price_per_month', 'description', 'duration_in_months']

class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ['user', 'plan', 'purchase_date', 'is_active']


class UserHistorySerializer(serializers.ModelSerializer):
    content_title = serializers.CharField(source="content.title", read_only=True)
    content_id = serializers.IntegerField(source="content.id", read_only=True)
    user_name = serializers.CharField(source='userprofile.username', read_only=True)
    user_id = serializers.IntegerField(source='userprofile.user.id', read_only=True)
    user_avatar = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = UserProfileContentInfo
        fields = [
            "id",
            "last_watch",
            "user_rating",
            "movie_progress",
            "episode_progress",
            "content_id",
            "content_title",  
            "comment",
            "comment_date",
            "cover_image",
            "user_name",
            "user_id",
            "user_avatar",
        ]
        read_only_fields = [
            "id",
            "last_watch",
            "movie_progress",
            "episode_progress",
            "content_id",
            "content_title",
            "comment_date",
            "user_name",
            "user_id",
            "user_avatar",
        ]
    
    def get_user_avatar(self, obj):
        request = self.context.get('request')
        if obj.userprofile.profile_picture:
            if hasattr(obj.userprofile.profile_picture, 'url'):
                return request.build_absolute_uri(obj.userprofile.profile_picture.url)
        return None

    def get_cover_image(self, obj):
        request = self.context.get('request')
        if obj.content and obj.content.cover_image:
            if hasattr(obj.content.cover_image, 'url'):
                return request.build_absolute_uri(obj.content.cover_image.url)
        return None

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'content', 'text', 'datetime']

class UserProfileNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()

    class Meta:
        model = UserProfileNotifications
        fields = ['id', 'userprofile', 'status', 'notification']

class UserProfileNotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileNotifications
        fields = ['status']