from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api_users.permissions import IsOwnProfileOrAdmin
from api_users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnProfileOrAdmin,)
    pagination_class = PageNumberPagination
    search_fields = ('=username',)
    lookup_field = 'username'

    def get_object(self):
        if self.kwargs.get('username') == 'me':
            return self.request.user

        return super(UserViewSet, self).get_object()

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username') == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, args, kwargs)
