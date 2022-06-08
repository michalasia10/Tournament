from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from tournament.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    profile_id = serializers.IntegerField(source='id')
    user_id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')

    class Meta():
        model = UserProfile
        fields = ('profile_id', 'user_id', 'username', 'birth', 'team')


class UserProfileUpdate(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta():
        model = UserProfile
        fields = ('username', 'team')

    def _get_user(self, username):
        return User.objects.get(username=username)

    def validate(self, data):
        username = data.get('username')
        try:
            self._get_user(username)

        except UserProfile.DoesNotExist:
            raise ValidationError("User Profile dosen't exist")

        return data

    def save(self):
        user = self._get_user(self.validated_data['username'])

        if user.is_superuser:
            raise ValidationError("Can't append superuser to team")

        user_profile = UserProfile.objects.get(user_id=user.id)
        user_profile.team = self.validated_data['team']
        user_profile.save()

        return user_profile
