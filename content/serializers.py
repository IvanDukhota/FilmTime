from rest_framework import serializers
from DataBase.models import (
    Content,
    Genre,
    Actor,
    ContentActor,
    ContentList,
    Series,
    Season,
    Episode,
    Movie,
    Director,  
    ContentDirector,
    ContentList,
    Content,
    List
)


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
    content_title = serializers.CharField(source="content.title", read_only=True)
    content_id = serializers.IntegerField(source="content.id", read_only=True)
    content_type = serializers.CharField(source="content.content_type", read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = ContentList
        fields = ['id', 'content_title', 'content_id', 'content_type', 'cover_image']

    def get_cover_image(self, obj):
        request = self.context.get('request')
        if obj.content and obj.content.cover_image and hasattr(obj.content.cover_image, 'url'):
            return request.build_absolute_uri(obj.content.cover_image.url)
        return None


class ListSerializer(serializers.ModelSerializer):
    contents = ContentListSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ['id', 'list_name', 'userprofile', 'create_date', 'contents']


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


class DirectorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Director
        fields = ["id", "name"]


class ContentSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()
    movie = MovieSerializer(read_only=True)
    series = SeriesSerializer(read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = [
            "id",
            "title",
            "release_date",
            "content_type",
            "trailer_url",
            "synopsis",
            "directors",
            "genres",
            "actors",
            "movie",
            "series",
            "cover_image",
        ]

    def get_genres(self, obj):
        genres = Genre.objects.filter(contentgenres__content=obj)
        return GenreSerializer(genres, many=True).data

    def get_actors(self, obj):
        actors = Actor.objects.filter(contentactor__content=obj)
        return ActorSerializer(actors, many=True).data

    def get_directors(self, obj):
        directors = Director.objects.filter(contentdirector__content=obj)
        return DirectorSerializer(directors, many=True).data

    def get_cover_image(self, obj):
        request = self.context.get('request')
        if obj.cover_image and hasattr(obj.cover_image, 'url'):
            return request.build_absolute_uri(obj.cover_image.url)
        return None
