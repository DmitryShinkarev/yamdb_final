from rest_framework.routers import DefaultRouter

from api_users.views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
