from rest_framework import serializers

from tournament.models import Stage


class StageSerializer(serializers.ModelSerializer):
    tournament_name = serializers.CharField(source='tourament.name')
    winner = serializers.CharField(source='winner.name',default=None)
    class Meta():
        model = Stage
        fields = ('id', 'stage_part', 'group_name', 'tourament', 'tournament_name', 'winner')
