from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tournament.models import Stage, Match, StatusEnum
from tournament.serializers import StageSerializer


class StagesModelViewSet(ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer

    def _winner(self, match: Match) -> int:
        winner: str = max(match.score, key=match.score.get)
        team = getattr(match, winner)
        return team

    @action(detail=False, methods=["GET"])
    def check_winners(self, request, *args, **kwargs):
        stages = self.get_queryset()

        stage: Stage
        for stage in stages:
            if stage.matches.exists():
                match: Match = stage.matches.first()

                if match.status == StatusEnum.END.value:
                    winner = self._winner(match)
                    stage.winner = winner
                    stage.save()

        data = self.get_queryset()
        serializer = StageSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
