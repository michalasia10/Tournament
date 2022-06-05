from rest_framework import serializers
from tournament.models import Team


class TeamSerializerCreate(serializers.ModelSerializer):
    class Meta():
        model = Team
        fields = ('name', 'color')

    def create(self, validated_data):
        return Team.objects.create(**validated_data)
