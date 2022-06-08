from rest_framework.viewsets import ModelViewSet

from tournament.models import UserProfile
from tournament.serializers import UserProfileSerializer


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
