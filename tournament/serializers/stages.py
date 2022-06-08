from rest_framework import serializers

from tournament.models import Stage


class StageSerializer(serializers.ModelSerializer):
    class Meta():
        model = Stage
        fields = ('stage_part', 'group_name', 'winner')
