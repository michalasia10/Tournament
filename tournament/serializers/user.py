from rest_framework import serializers
from tournament.models import UserProfile

from rest_framework.exceptions import ValidationError

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta():
        model = UserProfile
        fields = ('id','user', 'birth', 'team')


class UserProfileUpdate(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta():
        model = UserProfile
        fields = ('user_id','team')

    def validate(self, data):
        user_id = data.get('user_id')
        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            raise  ValidationError("User Profile dosen't exist")

        return data

    def save(self):
        user_profile =  UserProfile.objects.get(user_id=self.validated_data['user_id'])
        user_profile.team = self.validated_data['team']
        user_profile.save()
        return user_profile