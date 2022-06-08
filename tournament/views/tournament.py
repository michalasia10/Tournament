import random
from string import ascii_uppercase
from typing import List, Tuple, Union

from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tournament.models import Tournament, Stage, Match, Team
from tournament.serializers import TournamentSerializer, TournamentRetrieveSerializer, \
    TournamentSpecificStageSerializer, TournamentCreateQualifications


class TournamentViewSet(ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_classes = {
        'get_specific_stage': TournamentSpecificStageSerializer,
        'retrieve': TournamentRetrieveSerializer,
        'add_teams_add_generate_qualifications': TournamentCreateQualifications,
    }
    default_serializer_class = TournamentSerializer

    @staticmethod
    def team_have_players(team_id: Team.pk):
        return Team.objects.filter(players__isnull=True, pk=team_id).first() is None

    @classmethod
    def generate_enemies(self, teams: List[int]) -> Union[Tuple[dict, list], Tuple[bool, bool]]:
        try:
            enemies: List[int] = random.sample(teams, 2)
        except ValueError:
            return False, False

        for enemy_id in enemies:

            if not self.team_have_players(enemy_id):
                raise ValidationError(f"Team with ID ({enemy_id}) don't have players or doesn't exist")

        return {key: value for key, value in zip(["team_a_id", "team_b_id"], enemies)}, enemies

    @staticmethod
    def pop_enemies_from_team_list(teams: List[int], enemies: List[int]) -> List[int]:
        return [team for team in teams if team not in enemies]

    def create(self, request, *args, **kwargs):
        serializer = TournamentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        tournament_: Tournament = Tournament.objects.filter(**serializer.validated_data).first()

        num_stages = tournament_.max_teams // 2

        for num, letter in zip(range(num_stages), ascii_uppercase):
            Stage.objects.create(stage_part=0, tourament_id=tournament_.id, group_name=f'Qualifications_gr{letter}')

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
        serializer.is_valid(raise_exception=True)

        tournament_ = Tournament.objects.filter(pk=pk,
                                                stages__stage_part=serializer.validated_data['stage_part']).first()

        if tournament_ is None:
            raise ValidationError("No stage for current Tournament")

        serializer_response = TournamentRetrieveSerializer(tournament_)
        return Response(serializer_response.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True)
    def add_teams_add_generate_qualifications(self, request, pk=None):
        serializer = TournamentCreateQualifications(data=request.data)
        serializer.is_valid(raise_exception=True)

        teams_id: List[int] = serializer.validated_data.get('teams_id')
        tournament_: Tournament = self.get_object()

        if len(teams_id) >= tournament_.max_teams:
            raise ValidationError(f"This tournament has limit {tournament_.max_teams} of teams")

        stage: Stage
        for stage in tournament_.stages.all():
            enemies_dict, enemies_list = self.generate_enemies(teams_id)

            if not enemies_list:
                raise ValidationError(
                    "The tournament has only been partially set up or there is a complete lack of teams to stage")

            teams_id = self.pop_enemies_from_team_list(teams_id, enemies_list)

            try:
                Match.objects.create(stage_id=stage.id, **enemies_dict)

            except IntegrityError:
                raise ValidationError(f"Check if some of this teams is not in match {enemies_dict}")

        return Response("Qualification generated", status=status.HTTP_201_CREATED)
