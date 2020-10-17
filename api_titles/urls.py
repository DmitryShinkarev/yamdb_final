from rest_framework.routers import DefaultRouter

from api_titles.views import (CategoryViewSet,
                              GenreViewSet,
                              TitleViewSet,
                              ReviewViewSet,
                              CommentViewSet
                              )

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments',
)
