# Generated by Django 5.1.2 on 2024-11-01 14:56

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('actor_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('content_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('content_type', models.CharField(choices=[('Movie', 'Movie'), ('Series', 'Series'), ('Animation', 'Animation')], max_length=20)),
                ('trailer_url', models.URLField(blank=True, max_length=255)),
                ('rating', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentActor',
            fields=[
                ('content_actor_id', models.AutoField(primary_key=True, serialize=False)),
                ('character_name', models.CharField(blank=True, max_length=255)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.actor')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.content')),
            ],
        ),
        migrations.CreateModel(
            name='ContentDetail',
            fields=[
                ('content_details_id', models.AutoField(primary_key=True, serialize=False)),
                ('synopsis', models.TextField(blank=True)),
                ('duration_seconds', models.IntegerField(blank=True, null=True)),
                ('content_rating', models.CharField(blank=True, max_length=10)),
                ('content', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='registration.content')),
            ],
        ),
        migrations.CreateModel(
            name='ContentDirector',
            fields=[
                ('content_director_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.content')),
            ],
        ),
        migrations.CreateModel(
            name='ContentGenre',
            fields=[
                ('content_genre_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.content')),
            ],
        ),
        migrations.CreateModel(
            name='ContentHistory',
            fields=[
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('watch_date', models.DateTimeField(auto_now_add=True)),
                ('paused_at_second', models.IntegerField(blank=True, null=True)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.content')),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('director_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('list_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.content')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notification_id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('content', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.content')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('review_text', models.TextField(blank=True)),
                ('review_date', models.DateTimeField(auto_now_add=True)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.content')),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('subscription_plan_id', models.AutoField(primary_key=True, serialize=False)),
                ('plan_name', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('content_access_level', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(choices=[('user', 'User'), ('admin', 'Admin'), ('moderator', 'Moderator')], max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserList',
            fields=[
                ('list_id', models.AutoField(primary_key=True, serialize=False)),
                ('list_name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserPreferredGenre',
            fields=[
                ('user_preference_id', models.AutoField(primary_key=True, serialize=False)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.genre')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('profile_picture', models.BinaryField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('banned', 'Banned')], max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to='registration.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('subscription_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('subscription_plan', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='registration.subscriptionplan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.user')),
            ],
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.AddField(
            model_name='contentdirector',
            name='director',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.director'),
        ),
        migrations.AddField(
            model_name='contentgenre',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.genre'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.user'),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.user'),
        ),
        migrations.AddField(
            model_name='contenthistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.user'),
        ),
        migrations.AddField(
            model_name='listitem',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.userlist'),
        ),
    ]