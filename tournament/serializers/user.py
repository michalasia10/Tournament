from rest_framework import serializers
from tournament.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta():
        model = UserProfile
        fields = ('user', 'birth', 'team')