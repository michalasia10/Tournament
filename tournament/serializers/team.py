import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.settings import REGEX_TO_VALID_COLOR
from tournament.models import Team
from tournament.serializers import UserProfileSerializer


class TeamSerializer(serializers.ModelSerializer):
    players = UserProfileSerializer(many=True, read_only=True)

    class Meta():
        model = Team
        fields = ('id', 'name', 'color', 'players')


class TeamSerializerCreate(serializers.ModelSerializer):
    class Meta():
        model = Team
        fields = ('name', 'color')

    def create(self, validated_data):
        return Team.objects.create(**validated_data)

    def validate(self, data: dict):
        color: str = data.get('color', None)

        color_is_valid = re.match(REGEX_TO_VALID_COLOR, color)
        if color_is_valid:
            return data

        raise ValidationError("Your color is not valid hex color")
