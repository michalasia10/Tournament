from tournament.models import UserProfile
from tournament.serializers import UserProfileSerializer
from rest_framework.viewsets import ModelViewSet

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer