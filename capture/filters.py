import django_filters

from .models import Bookmark


class MultiValueCharFilter(django_filters.filters.BaseCSVFilter, django_filters.filters.CharFilter):
    def filter(self, qs, value):
        values = value or []
        for value in values:
            qs = super(MultiValueCharFilter, self).filter(qs, value)
        return qs

class BookmarkListFilter(django_filters.FilterSet):
    tags__name__exact = MultiValueCharFilter(name='tags__name', lookup_expr='exact')
    name__exact = MultiValueCharFilter(name='name', lookup_expr='exact')
    folderName__exact = MultiValueCharFilter(name='folderName', lookup_expr='exact')
    owner__username__exact = MultiValueCharFilter(name='owner__username', lookup_expr='exact')

    class Meta:
        model = Bookmark
        fields = {
            'tags__name': ['exact'],
            'name': ['exact'],
            'folderName': ['exact'],
            'owner__username': ['exact'],
        }