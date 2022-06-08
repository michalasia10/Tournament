from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tournament.models import Team
from tournament.serializers import TeamSerializerCreate, UserProfileUpdate, TeamSerializer


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_classes = {
        'list': TeamSerializer,
        'add_me_to_team': UserProfileUpdate,
        'add_user_to_team': UserProfileUpdate,
        'retrieve': TeamSerializer,
    }
    default_serializer_class = TeamSerializerCreate

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET'], )
    def add_me_to_team(self, request, pk=None):
        team = self.get_object()
        serializer = self.get_serializer_class()(data={'username': request.user.username, 'team': team.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(f"{request.user.username} added to {team.name}", status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def add_user_to_team(self, request, pk=None):
        team = self.get_object()
        serializer = self.get_serializer_class()(data={'username': request.data['username'], 'team': team.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(f"{request.data['username']} added to {team.name}", status=status.HTTP_201_CREATED)
