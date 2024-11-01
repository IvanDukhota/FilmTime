from rest_framework import serializers
from .models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_profile_id', 'user_id', 'username', 'profile_picture', 'country', 'bio', 'status']

class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['user_id', 'email', 'password_hash', 'date_joined', 'role', 'user_profile']
        extra_kwargs = {
            'password_hash': {'write_only': True},  # Password should not be exposed when retrieving the user
        }

    def create(self, validated_data):
        # Extract user_profile data
        user_profile_data = validated_data.pop('user_profile')
        # Create user instance
        user = User.objects.create(**validated_data)
        # Create UserProfile instance
        UserProfile.objects.create(user=user, **user_profile_data)
        return user

    def update(self, instance, validated_data):
        # Extract user_profile data
        user_profile_data = validated_data.pop('user_profile', None)
        
        # Update User instance
        instance.email = validated_data.get('email', instance.email)
        instance.password_hash = validated_data.get('password_hash', instance.password_hash)
        instance.role = validated_data.get('role', instance.role)
        instance.save()

        # Update UserProfile instance if it exists
        if user_profile_data:
            user_profile = instance.userprofile
            user_profile.username = user_profile_data.get('username', user_profile.username)
            user_profile.profile_picture = user_profile_data.get('profile_picture', user_profile.profile_picture)
            user_profile.country = user_profile_data.get('country', user_profile.country)
            user_profile.bio = user_profile_data.get('bio', user_profile.bio)
            user_profile.status = user_profile_data.get('status', user_profile.status)
            user_profile.save()

        return instance
