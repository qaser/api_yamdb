from django_filters import rest_framework as filters
from .models import Title
    
class TitleFilter(filters.FilterSet):
#    genre_slug = filters.CharFilter(field_name='genre__slug')
#    category_slug = filters.NumericRangeFilter(field_name="number", lookup_expr='lte')
    
    class Meta:
        model = Title
        fields = ['category', 'genre', 'year', 'name']