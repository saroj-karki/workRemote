import django_filters
from .choices import *
from .models import Post
from django_filters import ChoiceFilter, FilterSet


class PostFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(choices= JOB_CATEGORY, )

    class Meta:
        model = Post
        fields = ['category']
