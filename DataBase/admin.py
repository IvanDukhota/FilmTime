from django.contrib import admin
from .models import *


# UserProfile Model
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'user', 'status', 'country', 'bio')
    search_fields = ('username', 'user__email', 'status')
    list_filter = ('status',)


# User Model
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_staff', 'is_active')
    search_fields = ('email', 'role')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active')}),
    )

    ordering = ['email']


# Subscription Model
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'term_of_usage', 'purchase_date')
    search_fields = ('name', 'level')


# Genre Model
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# UserGenres Model
class UserGenresAdmin(admin.ModelAdmin):
    list_display = ('userprofile', 'genre')
    search_fields = ('userprofile__username', 'genre__name')


# Content Model
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'content_type', 'synopsis')
    search_fields = ('title', 'content_type', 'synopsis')
    list_filter = ('content_type',)


# Director Model
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ContentDirector Model
class ContentDirectorAdmin(admin.ModelAdmin):
    list_display = ('content', 'director')
    search_fields = ('content__title', 'director__name')


# ContentGenres Model
class ContentGenresAdmin(admin.ModelAdmin):
    list_display = ('content', 'genre')
    search_fields = ('content__title', 'genre__name')


# UserProfileContentInfo Model
class UserProfileContentInfoAdmin(admin.ModelAdmin):
    list_display = ('userprofile', 'content', 'user_rating', 'last_watch')
    search_fields = ('userprofile__username', 'content__title')
    list_filter = ('user_rating',)


# Notification Model
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('text', 'datetime')


# Movie Model
class MovieAdmin(admin.ModelAdmin):
    list_display = ('content', 'duration', 'critic_rating', 'content_url')
    search_fields = ('content__title', 'content_url')


# Series Model
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('content',)
    search_fields = ('content__title',)


# Seasons Model
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('series', 'number', 'release_date', 'critic_rating')
    search_fields = ('series__content__title',)
    list_filter = ('series',)


# Episode Model
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('season', 'number', 'title', 'release_date', 'critic_rating')
    search_fields = ('season__series__content__title', 'title')


# Actor Model
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ContentActor Model
class ContentActorAdmin(admin.ModelAdmin):
    list_display = ('content', 'actor', 'character_name')
    search_fields = ('content__title', 'actor__name', 'character_name')


# List Model
class ListAdmin(admin.ModelAdmin):
    list_display = ('userprofile', 'list_name', 'create_date')
    search_fields = ('userprofile__username', 'list_name')


# ContentList Model
class ContentListAdmin(admin.ModelAdmin):
    list_display = ('list', 'content')
    search_fields = ('list__list_name', 'content__title')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(UserGenres, UserGenresAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(ContentDirector, ContentDirectorAdmin)
admin.site.register(ContentGenres, ContentGenresAdmin)
admin.site.register(UserProfileContentInfo, UserProfileContentInfoAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(ContentActor, ContentActorAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(ContentList, ContentListAdmin)
