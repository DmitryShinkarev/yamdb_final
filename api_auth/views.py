from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_auth.serializers import (AuthenticationSerializer,
                                  RegistrationSerializer
                                  )

User = get_user_model()


class RegisterUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RegistrationSerializer


class ObtainTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = AuthenticationSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.data.get('email'))
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)},
                        status=status.HTTP_200_OK)
