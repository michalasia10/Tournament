from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from tournament.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ('username', 'email', 'password')


class RegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    birth = serializers.DateTimeField()

    class Meta():
        model = UserProfile
        fields = ('user', 'birth')

    def create(self, validated_data):
        user_data = validated_data['user']
        user = User.objects.create_user(**user_data)
        return UserProfile.objects.create(user=user, birth=validated_data['birth'])


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                data['user'] = user
            else:
                raise ValidationError("Unable to login with given credentials")
        else:
            raise ValidationError("Enter some data")

        return data
