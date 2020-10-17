from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api_titles.exceptions import ReviewExistsError
from api_titles.filters import TitleFilter
from api_titles.models import Category, Genre, Title, Review
from api_titles.permissions import (IsAdminOrReadOnly,
                                    IsModeratorOrAdmin,
                                    IsModeratorOrAdminOrAuthor,
                                    IsAuthor
                                    )
from api_titles.serializers import (CategorySerializer,
                                    GenreSerializer,
                                    TitleSerializer,
                                    ReviewSerializer,
                                    CommentSerializer
                                    )


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre'))
        category = get_object_or_404(
            Category, slug=self.request.data.get('category'))
        serializer.save(genre=genre, category=category, rating=None)

    def perform_update(self, serializer):
        kwargs = {}
        genre = self.request.data.getlist('genre')
        category = self.request.data.get('category')
        if genre:
            kwargs['genre'] = Genre.objects.filter(slug__in=genre)
        if category:
            kwargs['category'] = get_object_or_404(Category,
                                                   slug=self.request.
                                                   data.get('category'))
        serializer.save(**kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.request.method in ('POST', 'GET', 'PUT',):
            return [IsAuthenticatedOrReadOnly()]
        elif self.request.method == 'PATCH':
            return [IsModeratorOrAdminOrAuthor()]
        elif self.request.method == 'DELETE':
            return [IsModeratorOrAdmin()]

    def get_queryset(self, *args, **kwargs):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title,
                                  pk=self.kwargs.get('title_id'))
        if Review.objects.filter(title=title,
                                 author=self.request.user).exists():
            raise ReviewExistsError

        serializer.save(author=self.request.user, title=title)
        title.update_ratings()

    def perform_update(self, serializer):
        serializer.save()
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        title.update_ratings()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.request.method in ('POST', 'GET',):
            return [IsAuthenticatedOrReadOnly()]
        elif self.request.method == 'PUT':
            return [IsAuthor()]
        elif self.request.method == 'PATCH':
            return [IsModeratorOrAdminOrAuthor()]
        elif self.request.method == 'DELETE':
            return [IsModeratorOrAdmin()]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review,
                                   pk=self.kwargs.get('review_id'),
                                   title=title)
        return review.review_comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, title=title, review=review)
