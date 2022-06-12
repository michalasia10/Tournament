import random
from string import ascii_uppercase
from typing import List, Tuple, Union

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tournament.models import Tournament, StatusEnum, Stage, Match, Team
from tournament.serializers import TournamentSerializer, TournamentRetrieveSerializer, \
    TournamentSpecificStageSerializer, TournamentCreateQualifications, TournamentCreateSerializer


class TournamentViewSet(ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_classes = {
        'get_specific_stage': TournamentSpecificStageSerializer,
        'retrieve': TournamentRetrieveSerializer,
        'add_teams_add_generate_qualifications': TournamentCreateQualifications,
        'create': TournamentCreateSerializer,
    }
    default_serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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
        serializer = TournamentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        tournament_: Tournament = Tournament.objects.filter(**serializer.validated_data).first()

        num_stages = tournament_.max_teams // 2

        for num, letter in zip(range(num_stages), ascii_uppercase):
            Stage.objects.create(stage_part=0, tourament_id=tournament_.id, group_name=f'Qualifications_gr{letter}')
        serializer = self.default_serializer_class(tournament_)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TournamentRetrieveSerializer(instance)
        return Response(serializer.data)

    def _destroy(self, instance):
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None, *args, **kwargs):
        user: User = self.request.user
        tournament_: Tournament = self.get_object()

        if tournament_.owner == user:

            if tournament_.status == StatusEnum.START.value:
                raise ValidationError("You're tournamet begin you can't delte if you're not superuser",
                                      code=status.HTTP_401_UNAUTHORIZED)

            return self._destroy(tournament_)

        if tournament_.owner.is_superuser:
            return self._destroy(tournament_)

        raise ValidationError("You're not authorized to run this method", code=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['GET'], detail=True)
    def get_specific_stage(self, request, pk=None, *args, **kwargs):
        stage_part = request.query_params.get('stage_part')

        if stage_part is None:
            raise ValidationError("Bad query params, try with ?stage_part")

        tournament_ = Tournament.objects.filter(pk=pk,
                                                stages__stage_part=int(stage_part)).first()

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

        tournament_.status = StatusEnum.START.value
        return Response("Qualification generated", status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=False)
    def historic_tournaments(self, request, *args, **kwargs):
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)

        if start_time is None or end_time is None:
            tournaments = Tournament.objects.filter(status=StatusEnum.END.value).all()
            serializer = TournamentSerializer(tournaments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        tournaments = Tournament.objects.filter(status=StatusEnum.END.value, start_time__range=start_time,
                                                end_time__range=end_time).all()
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def end_tournament(self, request, pk):
        tournament = self.get_object()
        tournament.status = StatusEnum.END.value
        tournament.save()
        serializer = TournamentSerializer(tournament)
        return Response(serializer.data, status=status.HTTP_200_OK)
