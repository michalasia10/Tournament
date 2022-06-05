from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from tournament.serializers import RegisterSerializer, UserProfileSerializer
from tournament.models import UserProfile


class RegisterAPIView(ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = serializer.save()
        token = Token.objects.create(user=user_profile.user)

        return Response({"user": serializer.data,
                         "token": token.key}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
