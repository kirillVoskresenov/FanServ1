import django_filters
from django import forms
from django_filters import FilterSet
from .models import *

class PostFilter(FilterSet):

    date = django_filters.DateFilter(
        field_name='article_date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='gte',
        label='Date (beginning with)'
    )


    class Meta:
        model = Post
        fields = {
           'author': ['exact'],
           'title': ['icontains']
       }