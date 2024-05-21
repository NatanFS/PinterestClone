from django_filters import rest_framework as filters
from .models import Pin

class PinFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    user = filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    tags = filters.CharFilter(field_name='tags', lookup_expr='icontains')
    ordering = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('likes', 'likes'),
        )
    )

    class Meta:
        model = Pin
        fields = ['title', 'user', 'tags']

