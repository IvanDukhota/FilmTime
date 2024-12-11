from rest_framework import serializers
from DataBase.models import UserProfileContentInfo


# serializers.py

from rest_framework import serializers
from DataBase.models import UserProfileContentInfo

class UserHistorySerializer(serializers.ModelSerializer):
    content_title = serializers.CharField(source="content.title", read_only=True)
    content_id = serializers.IntegerField(source="content.id", read_only=True)
    user_name = serializers.CharField(source='userprofile.username', read_only=True)
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
        ]
    
    def validate_user_rating(self, value):
        if value is not None and not (1 <= value <= 5):
            raise serializers.ValidationError("Рейтинг должен быть в диапазоне от 1 до 5.")
        return value

    def validate_comment(self, value):
        if value is not None and len(value) > 500:
            raise serializers.ValidationError("Комментарий не может превышать 500 символов.")
        return value

    def get_cover_image(self, obj):
        request = self.context.get('request')
        if obj.content and obj.content.cover_image:
            if hasattr(obj.content.cover_image, 'url'):
                return request.build_absolute_uri(obj.content.cover_image.url)
        return None

