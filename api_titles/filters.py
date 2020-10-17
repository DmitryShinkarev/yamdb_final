from django_filters import rest_framework as filters

from api_titles.models import Genre, Title, Category


class TitleFilter(filters.FilterSet):
    genre = filters.ModelMultipleChoiceFilter(
        field_name='genre__slug',
        to_field_name='slug',
        queryset=Genre.objects.all()
    )
    category = filters.ModelChoiceFilter(to_field_name='slug',
                                         queryset=Category.objects.all())
    name = filters.CharFilter(lookup_expr='contains')
    year = filters.NumberFilter

    class Meta:
        fields = ('genre', 'category', 'year', 'name',)
        model = Title
