from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)

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
            'username': {'required': False},
            'profile_picture': {'required': False},
            'country': {'required': False},
            'bio': {'required': False},
            'status': {'read_only': True},
        }

class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "password",
            "date_joined",
            "role",
            "user_profile",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            },
        }

    def create(self, validated_data):
        # Extract user_profile data
        user_profile_data = validated_data.pop("user_profile")
        # Create user instance
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        # Create UserProfile instance
        UserProfile.objects.create(user=user, **user_profile_data)
        return user

    def update(self, instance, validated_data):
        # Extract user_profile data
        user_profile_data = validated_data.pop("user_profile", None)

        # Update User instance
        instance.email = validated_data.get("email", instance.email)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.role = validated_data.get("role", instance.role)
        instance.save()

        # Update UserProfile instance if it exists
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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_id'] = user.id
        token['role'] = user.role

        return token

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid email or password')

        data = super().validate(attrs)
        return data
