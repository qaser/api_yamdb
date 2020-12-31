from django_filters import rest_framework as filters

from .models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='iexact')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    year = filters.CharFilter(field_name='year', lookup_expr='iexact')
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )

    class Meta:
        fields = '__all__'
        model = Title
