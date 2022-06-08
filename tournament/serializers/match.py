from rest_framework import serializers

from tournament.models import Match
from tournament.validators.match import JSONMatchSchemaValidator
from tournament.validators.schemas import MATCH_JSON_SCHEMA


class MatchSerializer(serializers.ModelSerializer):
    team_a_id = serializers.IntegerField(source='team_a.id')
    team_b_id = serializers.IntegerField(source='team_b.id')
    team_a_name = serializers.CharField(source='team_a.name')
    team_b_name = serializers.CharField(source='team_b.name')

    class Meta():
        model = Match
        fields = ('id','team_a_id', 'team_a_name', 'team_b_id','team_b_name', 'score')


class MatchCreateSerializer(serializers.ModelSerializer):
    class Meta():
        model = Match
        fields = ('team_a', 'team_b', 'stage')

    def create(self, validated_data):
        return Match.objects.create(**validated_data)


class MatchUpdateSerializer(serializers.ModelSerializer):
    score = serializers.JSONField(validators=[JSONMatchSchemaValidator(limit_value=MATCH_JSON_SCHEMA)])

    class Meta():
        model = Match
        fields = ('id', 'score')
