from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from tournament.models import UserProfile
from tournament.serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer


class RegisterAPIView(ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        user_profile = serializer.save()
        token = Token.objects.create(user=user_profile.user)
        data = dict(serializer.data)
        data['token'] = token.key
        return Response(data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(ViewSet):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token = Token.objects.get(user=user)
        return Response({"token": token.key}, status=200)


class LogoutView(ViewSet):
    authentication_classes = [TokenAuthentication]

    def create(self, request):
        django_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
