from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from uuid import uuid4
import os


# User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


# User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=10,
        choices=[("user", "User"), ("admin", "Admin"), ("moderator", "Moderator")],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


def unique_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("profile_pictures", filename)


# UserProfile Model
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile"
    )
    username = models.CharField(max_length=32, unique=True)
    profile_picture = models.ImageField(
        upload_to=unique_upload_path, null=True, blank=True
    )
    country = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=[("active", "Active"), ("banned", "Banned")]
    )
    subscription = models.ForeignKey(
        "Subscription", on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        try:
            old_file = UserProfile.objects.get(pk=self.pk).profile_picture
            if old_file and old_file != self.profile_picture:
                if os.path.isfile(old_file.path):
                    os.remove(old_file.path)
        except UserProfile.DoesNotExist:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


# Subscription Model
class Subscription(models.Model):
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=20)
    term_of_usage = models.TextField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Genre Model
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# UserGenres Model
class UserGenres(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.userprofile} - {self.genre}"


def unique_upload_path_content(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("covers", filename)

# Content Model
class Content(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    content_type = models.CharField(
        max_length=10, choices=[("movie", "Movie"), ("series", "Series")]
    )
    trailer_url = models.URLField(null=True, blank=True)
    synopsis = models.TextField()
    directors = models.ManyToManyField('Director', through='ContentDirector')
    cover_image = models.ImageField(
        upload_to=unique_upload_path, null=True, blank=True
    )
    def __str__(self):
        return self.title


class Director(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class ContentDirector(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('content', 'director')

    def __str__(self):
        return f"{self.director.name} - {self.content.title}"


# ContentGenres Model
class ContentGenres(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content} - {self.genre}"


# UserProfileContentInfo Model
class UserProfileContentInfo(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    last_watch = models.DateTimeField(null=True, blank=True)
    user_rating = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    comment_date = models.DateTimeField(null=True, blank=True)
    movie_progress = models.IntegerField(null=True, blank=True)
    episode_progress = models.IntegerField(null=True, blank=True)
    comment_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.userprofile} - {self.content}"


# Notification Model
class Notification(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=[("read", "Read"), ("unread", "Unread")]
    )

    def __str__(self):
        return f"Notification for {self.userprofile}"


# Movies Model
class Movie(models.Model):
    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    duration = models.IntegerField()  # in seconds
    critic_rating = models.FloatField()
    content_url = models.URLField()

    def __str__(self):
        return self.content.title


# Series Model
class Series(models.Model):
    content = models.OneToOneField(Content, on_delete=models.CASCADE)

    def __str__(self):
        return self.content.title


# Seasons Model
class Season(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    number = models.IntegerField()
    release_date = models.DateField()
    critic_rating = models.FloatField()

    def __str__(self):
        return f"{self.series} - Season {self.number}"


# Episodes Model
class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    episode_url = models.URLField()
    duration = models.IntegerField()  # in seconds
    critic_rating = models.FloatField()

    def __str__(self):
        return f"{self.title} (Episode {self.number})"


# Actors Model
class Actor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# ContentActors Model
class ContentActor(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.actor.name} as {self.character_name} in {self.content.title}"


# List Model
class List(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.list_name} for {self.userprofile.username}"


# ContentList Model
class ContentList(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="contents")
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.list.list_name} - {self.content.title}"


