from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.forms.models import model_to_dict
from tournament.models import Tournament, Stage
from tournament.serializers import TournamentSerializer, TournamentRetrieveSerializer


class TournamentViewSet(ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def create(self, request, *args, **kwargs):
        serializer = TournamentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        tournament_: Tournament = Tournament.objects.filter(**serializer.validated_data).first()

        num_stages = tournament_.max_teams // 2

        for num in range(num_stages):
            Stage.objects.create(stage_part=0, tourament_id=tournament_.id, group_name='Eliminations')

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TournamentRetrieveSerializer(instance)
        return Response(serializer.data)
