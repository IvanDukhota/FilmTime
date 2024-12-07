from rest_framework import serializers
from DataBase.models import UserProfileContentInfo


class UserHistorySerializer(serializers.ModelSerializer):
    content_title = serializers.CharField(source="content.title", read_only=True)
    content_picture = serializers.ImageField(source="content.picture", read_only=True)

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
            "content_picture",  
        ]
