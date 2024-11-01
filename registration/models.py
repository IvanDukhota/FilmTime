# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=10,
        choices=[("user", "User"), ("admin", "Admin"), ("moderator", "Moderator")],
    )

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile"
    )
    username = models.CharField(max_length=32, unique=True)
    profile_picture = models.BinaryField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=[("active", "Active"), ("banned", "Banned")]
    )

    def __str__(self):
        return self.username


class Content(models.Model):
    CONTENT_TYPE_CHOICES = [
        ("Movie", "Movie"),
        ("Series", "Series"),
        ("Animation", "Animation"),
    ]

    content_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    release_date = models.DateField(blank=True, null=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    trailer_url = models.URLField(max_length=255, blank=True)
    rating = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ContentGenre(models.Model):
    content_genre_id = models.AutoField(primary_key=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content.title} - {self.genre.name}"


class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Director(models.Model):
    director_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ContentActor(models.Model):
    content_actor_id = models.AutoField(primary_key=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.content.title} - {self.actor.name} as {self.character_name}"


class ContentDirector(models.Model):
    content_director_id = models.AutoField(primary_key=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content.title} - Directed by {self.director.name}"


class SubscriptionPlan(models.Model):
    subscription_plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=255)
    price = models.FloatField()
    content_access_level = models.CharField(max_length=50)

    def __str__(self):
        return self.plan_name


class UserSubscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.RESTRICT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.subscription_plan.plan_name}"


class UserPreferredGenre(models.Model):
    user_preference_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.genre.name}"


class ContentHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    watch_date = models.DateTimeField(auto_now_add=True)
    paused_at_second = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} watched {self.content.title}"


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    review_text = models.TextField(blank=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} reviewed {self.content.title}"


class UserList(models.Model):
    list_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.email}'s List: {self.list_name}"


class ListItem(models.Model):
    list_item_id = models.AutoField(primary_key=True)
    list = models.ForeignKey(UserList, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.list.list_name} - {self.content.title}"


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.email}: {self.message}"


class ContentDetail(models.Model):
    content_details_id = models.AutoField(primary_key=True)
    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    synopsis = models.TextField(blank=True)
    duration_seconds = models.IntegerField(blank=True, null=True)
    content_rating = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.content.title} Details"


# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser


# class Actors(models.Model):
#     actor_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)

#     class Meta:
#         managed = False
#         db_table = "actors"


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         managed = False
#         db_table = "auth_group"


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = "auth_group_permissions"
#         unique_together = (("group", "permission"),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = "auth_permission"
#         unique_together = (("content_type", "codename"),)


# class AuthUser(AbstractBaseUser):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     date_joined = models.DateTimeField()

#     USERNAME_FIELD = "email"

#     class Meta:
#         managed = False
#         db_table = "auth_user"


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = "auth_user_groups"
#         unique_together = (("user", "group"),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = "auth_user_user_permissions"
#         unique_together = (("user", "permission"),)


# class Content(models.Model):
#     content_id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=255)
#     release_date = models.DateField(blank=True, null=True)
#     content_type = models.CharField(max_length=20)
#     trailer_url = models.CharField(max_length=255, blank=True, null=True)
#     rating = models.FloatField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = "content"


# class Contentactors(models.Model):
#     content_actor_id = models.AutoField(primary_key=True)
#     content = models.ForeignKey(Content, models.DO_NOTHING, blank=True, null=True)
#     actor = models.ForeignKey(Actors, models.DO_NOTHING, blank=True, null=True)
#     character_name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = "contentactors"


# class Contentdetails(models.Model):
#     content_details_id = models.AutoField(primary_key=True)
#     content = models.ForeignKey(Content, models.DO_NOTHING, blank=True, null=True)
#     synopsis = models.TextField(blank=True, null=True)
#     duration_seconds = models.IntegerField(blank=True, null=True)
#     content_rating = models.CharField(max_length=10, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = "contentdetails"


# class Contentdirectors(models.Model):
#     content_actor_id = models.AutoField(primary_key=True)
#     content = models.ForeignKey(Content, models.DO_NOTHING, blank=True, null=True)
#     director = models.ForeignKey("Directors", models.DO_NOTHING, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = "contentdirectors"


# class Contentgenres(models.Model):
#     content_genre_id = models.AutoField(primary_key=True)
#     content = models.ForeignKey(Content, models.DO_NOTHING, blank=True, null=True)
#     genre = models.ForeignKey("Genres", models.DO_NOTHING, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = "contentgenres"


# class Contenthistory(models.Model):
#     history_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey("Users", models.DO_NOTHING, blank=True, null=True)
#     content = models.ForeignKey(Content, models.DO_NOTHING, blank=True, null=True)
#     watch_date = models.DateTimeField(blank=True, null=True)
#     paused_at_second = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = "contenthistory"


# class Directors(models.Model):
#     director_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)

#     class Meta:
#         managed = False
#         db_table = "directors"


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.SmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey(
#         "DjangoContentType", models.DO_NOTHING, blank=True, null=True
#     )
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = "django_admin_log"


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = "django_content_type"
#         unique_together = (("app_label", "model"),)


# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = "django_migrations"


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = "django_session"


# class Genres(models.Model):
#     genre_id = models.AutoField(primary_key=True)
#     name = models.CharField(unique=True, max_length=100)

#     class Meta:
#         managed = False
#         db_table = "genres"


# class Listitems(models.Model):
#     list_item_id = models.AutoField(primary_key=True)
#     list = models.ForeignKey("Userlists", models.DO_NOTHING, blank=True, null=True)
#     content = models.ForeignKey(Content, models.DO_NOTHING, blank=True, null=True)
#     date_added = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = "listitems"


# class Notifications(models.Model):
#     notification_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey("Users", models.DO_NOTHING, blank=True, null=True)
#     content = models.ForeignKey(Content, models.DO_NOTHING, blank=True, null=True)
#     message = models.TextField()
#     date_sent = models.DateTimeField(blank=True, null=True)
#     is_read = models.BooleanField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = "notifications"


# class RegistrationCustomer(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     last_login = models.DateTimeField(blank=True, null=True)
#     username = models.CharField(unique=True, max_length=50)
#     email = models.CharField(unique=True, max_length=254)
#     password = models.CharField(max_length=128)
#     date_joined = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = "registration_customer"


# class Reviews(models.Model):
#     review_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey("Users", models.DO_NOTHING, blank=True, null=True)
#     content = models.ForeignKey(Content, models.DO_NOTHING, blank=True, null=True)
#     rating = models.FloatField(blank=True, null=True)
#     review_text = models.TextField(blank=True, null=True)
#     review_date = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = "reviews"


# class Subscriptionplans(models.Model):
#     subscription_plan_id = models.AutoField(primary_key=True)
#     plan_name = models.CharField(max_length=255)
#     price = models.FloatField()
#     content_access_level = models.CharField(max_length=50)

#     class Meta:
#         managed = False
#         db_table = "subscriptionplans"


# class Userlists(models.Model):
#     list_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey("Users", models.DO_NOTHING, blank=True, null=True)
#     list_name = models.CharField(max_length=255)

#     class Meta:
#         managed = False
#         db_table = "userlists"


# class Userpreferredgenres(models.Model):
#     user_preference_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey("Users", models.DO_NOTHING, blank=True, null=True)
#     genre = models.ForeignKey(Genres, models.DO_NOTHING, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = "userpreferredgenres"


# class Userprofiles(models.Model):
#     user_profile_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey("Users", models.DO_NOTHING, blank=True, null=True)
#     username = models.CharField(unique=True, max_length=32)
#     profile_picture = models.BinaryField(blank=True, null=True)
#     country = models.CharField(max_length=100, blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     status = models.CharField(max_length=10)

#     class Meta:
#         managed = False
#         db_table = "userprofiles"


# class Users(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     email = models.CharField(unique=True, max_length=32)
#     password_hash = models.CharField(max_length=255)
#     date_joined = models.DateTimeField(blank=True, null=True)
#     role = models.CharField(max_length=10)

#     class Meta:
#         managed = False
#         db_table = "users"


# class Usersubscriptions(models.Model):
#     subscription_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
#     subscription_plan = models.ForeignKey(
#         Subscriptionplans, models.DO_NOTHING, blank=True, null=True
#     )
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField(blank=True, null=True)
#     is_active = models.BooleanField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = "usersubscriptions"
