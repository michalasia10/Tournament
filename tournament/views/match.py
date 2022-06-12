from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tournament.models import Match
from tournament.serializers import MatchSerializer, MatchUpdateSerializer, MatchCreateSerializer


class MatchModelViewSet(ModelViewSet):
    queryset = Match.objects.all()
    serializer_classes = {
        'create': MatchCreateSerializer,
        'update': MatchUpdateSerializer,
        'change_score_for_match': MatchUpdateSerializer,
    }
    default_serializer_class = MatchSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PUT'])
    def change_score_for_match(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        match: Match = self.get_object()
        match.score = serializer.validated_data['score']
        match.save()

        return Response(self.default_serializer_class(match), status=status.HTTP_200_OK)
