from django.utils.translation import gettext_lazy as _
from .models import Tour, Activity, Continent, Country, Region, TourEvent,\
    Place, TourObject, Route, GuideProfile, DifficultyLevel, PhysicalLevel, Refuge, Calendar
import django.forms
from django.db.models import Q
import django_filters


class CalendarFilter(django_filters.FilterSet):
    tour__tourevent__route__activity = django_filters.ModelMultipleChoiceFilter(
        queryset=Activity.active.filter(
            route__in=Route.active.filter(
                tourevent__in=TourEvent.objects.filter(tour__in=Tour.active.all())
            )
        ).distinct(),
        label=_('Activity')
    )
    tour__tourevent__route__place__region__country__continent = django_filters.ModelMultipleChoiceFilter(
        queryset=Continent.active.filter(
            country__in=Country.active.filter(
                region__in=Region.active.filter(
                    place__in=Place.active.filter(
                        route__in=Route.active.filter(
                            tourevent__in=TourEvent.objects.filter(tour__in=Tour.active.all())
                        )
                    )
                )
            )
        ).distinct(),
        label=_('Continent')
    )
    tour__tourevent__route__place__region__country = django_filters.ModelMultipleChoiceFilter(
        queryset=Country.active.filter(
            region__in=Region.active.filter(
                place__in=Place.active.filter(
                    route__in=Route.active.filter(
                        tourevent__in=TourEvent.objects.filter(tour__in=Tour.active.all())
                    )
                )
            )
        ).distinct(),
        label=_('Country')
    )
    tour__tourevent__route__place__region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.active.filter(
            place__in=Place.active.filter(
                route__in=Route.active.filter(
                    tourevent__in=TourEvent.objects.filter(tour__in=Tour.active.all())
                )
            )
        ).distinct(),
        label=_('Region')
    )
    tour__tourevent__route__place = django_filters.ModelMultipleChoiceFilter(
        queryset=Place.active.filter(
            route__in=Route.active.filter(
                tourevent__in=TourEvent.objects.filter(tour__in=Tour.active.all())
            )
        ).distinct(),
        label=_('Place')
    )
    tour__tourevent__route__refuge = django_filters.ModelMultipleChoiceFilter(
        queryset=Refuge.active.filter(
            route__in=Route.active.filter(
                tourevent__in=TourEvent.objects.filter(tour__in=Tour.active.all())
            )
        ).distinct(),
        label=_('Refuge')
    )
    tour__guide = django_filters.ModelMultipleChoiceFilter(
        queryset=GuideProfile.active.filter(tour__in=Tour.active.all()).distinct()
    )
    tour__tourevent__route__difficulty_level = django_filters.ModelMultipleChoiceFilter(
        queryset=DifficultyLevel.objects.filter(
            route__in=Route.active.filter(tourevent__in=TourEvent.objects.filter(tour__in=Tour.active.all()))
        ).distinct(),
        label=_('Difficulty Level')
    )
    tour__tourevent__route__physical_level = django_filters.ModelMultipleChoiceFilter(
        queryset=PhysicalLevel.objects.filter(
            route__in=Route.active.filter(tourevent__in=TourEvent.objects.filter(tour__in=Tour.active.all()))
        ).distinct(),
        label=_('Physical Level')
    )
    tour__price = django_filters.NumberFilter()
    tour__price__gt = django_filters.NumberFilter(field_name='tour__price', lookup_expr='gte', label=_('Price min'))
    tour__price__lt = django_filters.NumberFilter(field_name='tour__price', lookup_expr='lte', label=_('Price max'))
    start_date = django_filters.DateFilter(
        field_name='start_date',
        lookup_expr='gt',
        label=_('Date from'),
        widget=django.forms.DateInput(
            attrs={'type': 'date'}
        )
    )
    end_date = django_filters.DateFilter(
        field_name='end_date',
        lookup_expr='lt',
        label=_('Date through'),
        widget=django.forms.DateInput(
            attrs={'type': 'date'}
        )
    )
    search = django_filters.CharFilter(method='calendar_search_filter', label=_('Search'))
    tour__tourevent__tour_object = django_filters.ModelMultipleChoiceFilter(
        queryset=TourObject.active.filter(tourevent__in=TourEvent.objects.filter(tour__in=Tour.active.all())).distinct(),
        label=_('Tour Object')
    )
    tour__tourevent__route = django_filters.ModelMultipleChoiceFilter(
        queryset=Route.active.filter(tourevent__in=TourEvent.objects.filter(tour__in=Tour.active.all())).distinct(),
        label=_('Route')
    )
    o = django_filters.OrderingFilter(
        fields=(
            ('start_date', 'start_date'),
            ('end_date', 'end_date'),
            ('tour__name', 'name'),
            ('tour__price', 'price'),
            ('tour__tourevent__route__difficulty_level', 'difficulty_level'),
            ('tour__tourevent__route__physical_level', 'physical_level'),
        ),
        field_labels={
            'tour__tourevent__route__difficulty_level': 'Difficulty',
            'tour__tourevent__route__physical_level': 'Physical',
        }
    )

    class Meta:
        model = Calendar
        fields = ['tour__tourevent__route__activity', 'tour__tourevent__route__place__region__country__continent',
                  'tour__tourevent__route__place__region__country', 'tour__tourevent__route__place__region',
                  'tour__tourevent__route__place', 'start_date', 'end_date', 'tour__tourevent__route__refuge',
                  'tour__guide', 'tour__price__gt', 'tour__price__lt', 'tour__tourevent__route__difficulty_level',
                  'tour__tourevent__route__physical_level', 'search', 'tour__tourevent__tour_object',
                  'tour__tourevent__route']

    def calendar_search_filter(self, queryset, name, value):
        return Calendar.objects.filter(
            Q(tour__name__icontains=value) | Q(tour__description__icontains=value) |
            Q(tour__tourevent__route__place__region__country__continent__name__icontains=value) |
            Q(tour__tourevent__route__place__region__country__name__icontains=value) |
            Q(tour__tourevent__route__place__region__name__icontains=value) |
            Q(tour__tourevent__route__place__name__icontains=value) |
            Q(tour__tourevent__route__activity__name__icontains=value) |
            Q(tour__guide__name__icontains=value) | Q(tour__tourevent__route__refuge__name__icontains=value) |
            Q(tour__tourevent__tour_object__name__icontains=value) | Q(tour__tourevent__route__name__icontains=value)
        ).distinct()
