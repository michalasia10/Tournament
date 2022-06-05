from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        password = make_password(validated_data['user'].pop('password'))
        return User.objects.create_user(**validated_data.pop('user'), password=password)
