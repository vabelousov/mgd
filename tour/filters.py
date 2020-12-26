from .models import Tour, Activity, Continent, Country, Region,\
    Place, TourObject, Route, Touring, GuideProfile, DifficultyLevel,\
    PhysicalLevel

import django.forms
from django.db.models import Q
import django_filters

class TourFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='my_custom_filter', label='Search')
    activity = django_filters.ModelMultipleChoiceFilter(
        queryset=Activity.active.filter(tour__in=Tour.active.all()).distinct()
    )
    continent = django_filters.ModelMultipleChoiceFilter(
        queryset=Continent.active.filter(tour__in=Tour.active.all()).distinct()
    )
    country = django_filters.ModelMultipleChoiceFilter(
        queryset=Country.active.filter(tour__in=Tour.active.all()).distinct()
    )
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.active.filter(tour__in=Tour.active.all()).distinct()
    )
    place = django_filters.ModelMultipleChoiceFilter(
        queryset=Place.active.filter(tour__in=Tour.active.all()).distinct()
    )
    tour_object = django_filters.ModelMultipleChoiceFilter(
        queryset=TourObject.active.filter(tour__in=Tour.active.all()).distinct()
    )
    route = django_filters.ModelMultipleChoiceFilter(
        queryset=Route.active.filter(tour__in=Tour.active.all()).distinct()
    )
    touring = django_filters.ModelMultipleChoiceFilter(
        queryset=Touring.active.filter(tour__in=Tour.active.all()).distinct()
    )
    guide = django_filters.ModelMultipleChoiceFilter(
        queryset=GuideProfile.active.filter(tour__in=Tour.active.all()).distinct()
    )
    difficulty_level = django_filters.ModelMultipleChoiceFilter(
        queryset=DifficultyLevel.objects.filter(tour__in=Tour.active.all()).distinct()
    )
    physical_level = django_filters.ModelMultipleChoiceFilter(
        queryset=PhysicalLevel.objects.filter(tour__in=Tour.active.all()).distinct()
    )
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Price min')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Price max')
    from_date = django_filters.DateFilter(
        field_name='start_date',
        lookup_expr='gt',
        label='Date from',
        widget=django.forms.DateInput(
            attrs={'type': 'date'}
        )
    )
    through_date = django_filters.DateFilter(
        field_name='end_date',
        lookup_expr='lt',
        label='Date through',
        widget=django.forms.DateInput(
            attrs={'type': 'date'}
        )
    )
    class Meta:
        model = Tour
        fields = ['search', 'activity', 'continent', 'country', 'region',
                  'place', 'tour_object', 'route', 'touring', 'guide', 'price__gt', 'price__lt',
                  'from_date', 'through_date', 'difficulty_level', 'physical_level']

    def my_custom_filter(self, queryset, name, value):
        return Tour.objects.filter(
            Q(name__icontains=value) | Q(description__icontains=value) | Q(country__name__icontains=value) | Q(place__name__icontains=value)
            | Q(activity__name__icontains=value) | Q(region__name__icontains=value) | Q(continent__name__icontains=value)
            | Q(tour_object__name__icontains=value) | Q(route__name__icontains=value) | Q(touring__name__icontains=value)
            | Q(guide__name__icontains=value)
        ).distinct()
