from rest_framework import serializers
from django.contrib.auth.models import User
from tournament.models import UserProfile
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    birth = serializers.DateTimeField()

    class Meta():
        fields = ('username', 'email', 'password', 'birth')

    def create(self, validated_data):
        password = make_password(validated_data['password'])
        validated_data['password'] = password
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'],
                                        email=validated_data['email'])
        return UserProfile.objects.create(user_id=user.id, birth=validated_data['birth'])


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta():
        model = UserProfile
        fields = ('user', 'birth', 'team')
