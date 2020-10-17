from rest_framework.routers import DefaultRouter

from api_auth.views import RegisterUserViewSet, ObtainTokenViewSet

router = DefaultRouter()
router.register('auth/token', ObtainTokenViewSet, basename='obtain_token')
router.register('auth/email', RegisterUserViewSet, basename='register_user')
