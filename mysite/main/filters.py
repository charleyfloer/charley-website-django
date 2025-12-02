import django_filters
from .models import Comments

class CommentsFilter(django_filters.FilterSet):
    article__title = django_filters.CharFilter(field_name='article__title', lookup_expr='icontains')

    class Meta:
        model = Comments
        fields = ['article__title', 'author']