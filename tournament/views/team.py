from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from tournament.models import Team
from tournament.serializers import TeamSerializerCreate, UserProfileUpdate


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializerCreate

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


    @action(detail=True,methods=['GET'],serializer_class=UserProfileUpdate)
    def add_me_to_team(self,request,pk=None):
        team = self.get_object()
        serializer = UserProfileUpdate(data={'user_id':request.user.id +1 ,'team':team.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)



    @action(detail=True,methods=['POST'],serializer_class=UserProfileUpdate)
    def add_user_to_team(self,request,pk=None):
        team = self.get_object()
        serializer = self.serializer_class(data={'user_id': request.data['user_id'], 'team': team.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

