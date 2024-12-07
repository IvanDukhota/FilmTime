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
    content_id = serializers.IntegerField(source="content.id", write_only=True)
    userprofile_username = serializers.CharField(source="userprofile.username", read_only=True)

    class Meta:
        model = ContentList
        fields = ['id', 'userprofile', 'content', 'list_name', 'create_date', 'content_title', 'content_id', 'userprofile_username']

    def create(self, validated_data):
        userprofile = self.context['request'].user.userprofile

        content = Content.objects.get(id=validated_data['content'].id)

        existing_content = ContentList.objects.filter(
            content=content,
            list_name=validated_data['list_name'],
            userprofile=userprofile
        ).exists()

        if existing_content:
            raise serializers.ValidationError("This content is already in the specified list.")

        content_list = ContentList.objects.create(
            userprofile=userprofile,
            content=content,
            list_name=validated_data['list_name']
        )
        return content_list



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