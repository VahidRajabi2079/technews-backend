from django_filters import rest_framework as filters
from django.db.models import Q
from .models import News

# فیلتر شخصی‌سازی‌شده برای دریافت لیست از رشته‌ها
class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class NewsFilter(filters.FilterSet):
    tags = CharInFilter(
        field_name='tags__name',
        lookup_expr='in',
        label='List of tag names'
    )
    keyword = filters.CharFilter(
        method='filter_by_keyword',
        label='Keyword in title/body'
    )
    exclude = filters.CharFilter(
        method='exclude_by_keyword',
        label='Exclude keyword from title/body'
    )

    class Meta:
        model = News
        fields = ['tags', 'keyword', 'exclude']

    def filter_by_keyword(self, queryset, filter_name, value):
        """فیلتر اخبار شامل کلیدواژه در عنوان یا متن"""
        if value:
            return queryset.filter(
                Q(title__icontains=value) | Q(body__icontains=value)
            )
        return queryset

    def exclude_by_keyword(self, queryset, filter_name, value):
        """حذف اخبار شامل کلیدواژه در عنوان یا متن"""
        if value:
            return queryset.exclude(
                Q(title__icontains=value) | Q(body__icontains=value)
            )
        return queryset
