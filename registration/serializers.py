from django.contrib.auth import authenticate
from rest_framework import serializers
from DataBase.models import (
    User,
    UserProfile,
    Content,
    Genre,
    Actor,
    ContentActor,
    ContentList,
    Series,
    Season,
    Episode,
    Movie,
    UserProfileContentInfo,
    Subscription,
)


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    profile_picture = serializers.ImageField(allow_empty_file=True, required=False)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user_id",
            "username",
            "profile_picture",
            "country",
            "bio",
            "status",
        ]
        extra_kwargs = {
            "username": {"required": False},
            "profile_picture": {"required": False},
            "country": {"required": False},
            "bio": {"required": False},
            "status": {"read_only": True},
        }


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "date_joined",
            "role",
            "user_profile",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user_profile_data = validated_data.pop("user_profile")
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        UserProfile.objects.create(user=user, **user_profile_data)
        return user

    def update(self, instance, validated_data):
        user_profile_data = validated_data.pop("user_profile", None)
        instance.email = validated_data.get("email", instance.email)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.role = validated_data.get("role", instance.role)
        instance.save()

        if user_profile_data:
            user_profile = instance.userprofile
            user_profile.username = user_profile_data.get(
                "username", user_profile.username
            )
            user_profile.profile_picture = user_profile_data.get(
                "profile_picture", user_profile.profile_picture
            )
            user_profile.country = user_profile_data.get(
                "country", user_profile.country
            )
            user_profile.bio = user_profile_data.get("bio", user_profile.bio)
            user_profile.status = user_profile_data.get("status", user_profile.status)
            user_profile.save()

        return instance


class CustomTokenObtainPairSerializer(serializers.Serializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)  # type: ignore
        token["user_id"] = user.id
        token["role"] = user.role
        return token

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )
        if user is None:
            raise serializers.ValidationError("Invalid email or password")
        data = super().validate(attrs)
        return data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "name"]


class ContentActorSerializer(serializers.ModelSerializer):
    actor = ActorSerializer()

    class Meta:
        model = ContentActor
        fields = ["id", "content", "actor", "character_name"]


class ContentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentList
        fields = ["id", "userprofile", "content", "list_name", "create_date"]


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "content", "duration", "critic_rating", "content_url"]


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ["id", "series", "number", "release_date", "critic_rating"]


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ["id", "season", "number", "release_date", "title", "duration"]


class SeriesSerializer(serializers.ModelSerializer):
    seasons = SeasonSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = ["id", "content", "seasons"]


class ContentSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = [
            "id",
            "title",
            "release_date",
            "content_type",
            "trailer_url",
            "synopsis",
            "director_name",
            "genres",
            "actors",
        ]

    def get_genres(self, obj):
        genres = Genre.objects.filter(contentgenres__content=obj)
        return GenreSerializer(genres, many=True).data

    def get_actors(self, obj):
        actors = Actor.objects.filter(contentactor__content=obj)
        return ActorSerializer(actors, many=True).data


class UserProfileContentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileContentInfo
        fields = [
            "id",
            "userprofile",
            "content",
            "last_watch",
            "user_rating",
            "comment",
            "comment_date",
            "movie_progress",
            "episode_progress",
        ]
