from rest_framework import serializers
from tournament.models import Tournament
from tournament.serializers import StageSerializer

class TournamentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Tournament
        fields = ('id','name', 'game_type', 'start_time', 'end_time','max_teams', 'max_players')


class TournamentCreateSerializer(TournamentSerializer):

    def create(self, validated_data):
        return Tournament.objects.create(**validated_data)

class TournamentRetrieveSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True,read_only=True)
    class Meta():
        model = Tournament
        fields = ('name', 'game_type', 'start_time', 'end_time', 'stages')


class TournamentSpecificStageSerializer(serializers.Serializer):
    stage_part = serializers.IntegerField()

    class Meta():
        fields = ('stage_part')