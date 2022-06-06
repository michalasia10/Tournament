from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tournament.models import Tournament, Stage
from tournament.serializers import TournamentSerializer, TournamentRetrieveSerializer, TournamentSpecificStageSerializer


class TournamentViewSet(ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_classes = {
        'get_specific_stage': TournamentSpecificStageSerializer,
        'retrieve': TournamentRetrieveSerializer
    }
    default_serializer_class = TournamentSerializer

    def create(self, request, *args, **kwargs):
        serializer = TournamentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        tournament_: Tournament = Tournament.objects.filter(**serializer.validated_data).first()

        num_stages = tournament_.max_teams // 2

        for num in range(num_stages):
            Stage.objects.create(stage_part=0, tourament_id=tournament_.id, group_name='Eliminations')

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TournamentRetrieveSerializer(instance)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def get_specific_stage(self, request, pk=None, *args, **kwargs):
        serializer = TournamentSpecificStageSerializer(data=request.data)
        serializer.is_valid()

        tournament_ = Tournament.objects.filter(pk=pk,
                                                stages__stage_part=serializer.validated_data['stage_part']).first()

        if tournament_ is None:
            raise ValidationError("No stage for current Tournament")

        serializer_response = TournamentRetrieveSerializer(tournament_)
        return Response(serializer_response.data, status=status.HTTP_200_OK)
