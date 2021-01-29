from django.utils.translation import gettext_lazy as _
from .models import Tour, Activity, Continent, Country, Region, TourEvent,\
    Place, TourObject, Route, GuideProfile, DifficultyLevel, PhysicalLevel, Refuge, Calendar
import django.forms
from django.db.models import Q
import django_filters


class CalendarFilter(django_filters.FilterSet):
    tour__activity = django_filters.ModelMultipleChoiceFilter(
        queryset=Activity.active.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Activity')
    )
    tour__continent = django_filters.ModelMultipleChoiceFilter(
        queryset=Continent.active.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Continent')
    )
    tour__country = django_filters.ModelMultipleChoiceFilter(
        queryset=Country.active.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Country')
    )
    tour__region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.active.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Region')
    )
    tour__place = django_filters.ModelMultipleChoiceFilter(
        queryset=Place.active.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Place')
    )
    tour__refuge = django_filters.ModelMultipleChoiceFilter(
        queryset=Refuge.active.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Refuge')
    )
    tour__guide = django_filters.ModelMultipleChoiceFilter(
        queryset=GuideProfile.active.filter(tour__in=Tour.active.all()).distinct()
    )
    tour__difficulty_level = django_filters.ModelMultipleChoiceFilter(
        queryset=DifficultyLevel.objects.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Difficulty Level')
    )
    tour__physical_level = django_filters.ModelMultipleChoiceFilter(
        queryset=PhysicalLevel.objects.filter(tour__in=Tour.active.all()).distinct(),
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
            ('tour__difficulty_level', 'difficulty_level'),
            ('tour__physical_level', 'physical_level'),
        ),
        field_labels={
            'tour__difficulty_level': 'Difficulty',
            'tour__physical_level': 'Physical',
        }
    )

    class Meta:
        model = Calendar
        fields = ['tour__activity', 'tour__continent', 'tour__country', 'tour__region', 'tour__place', 'start_date',
                  'end_date', 'tour__refuge', 'tour__guide', 'tour__price__gt', 'tour__price__lt',
                  'tour__difficulty_level', 'tour__physical_level', 'search', 'tour__tourevent__tour_object',
                  'tour__tourevent__route']

    def calendar_search_filter(self, queryset, name, value):
        return Calendar.objects.filter(
            Q(tour__name__icontains=value) | Q(tour__description__icontains=value) |
            Q(tour__country__name__icontains=value) | Q(tour__place__name__icontains=value) |
            Q(tour__activity__name__icontains=value) | Q(tour__region__name__icontains=value) |
            Q(tour__continent__name__icontains=value)| Q(tour__guide__name__icontains=value) |
            Q(tour__refuge__name__icontains=value) | Q(tour__tourevent__tour_object__name__icontains=value) |
            Q(tour__tourevent__route__name__icontains=value)
        ).distinct()


class TourFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='my_custom_filter', label=_('Search'))
    activity = django_filters.ModelMultipleChoiceFilter(
        queryset=Activity.active.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Activity')
    )
    continent = django_filters.ModelMultipleChoiceFilter(
        queryset=Continent.active.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Continent')
    )
    country = django_filters.ModelMultipleChoiceFilter(
        queryset=Country.active.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Country')
    )
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.active.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Region')
    )
    place = django_filters.ModelMultipleChoiceFilter(
        queryset=Place.active.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Place')
    )
    refuge = django_filters.ModelMultipleChoiceFilter(
        queryset=Refuge.active.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Refuge')
    )
    #  проблемный код -------
    tour_object = django_filters.ModelMultipleChoiceFilter(
        queryset=TourObject.active.filter(tourevent__in=TourEvent.objects.filter(tour__in=Tour.active.all())),
        label=_('Tour Object')
    )
    route = django_filters.ModelMultipleChoiceFilter(
        queryset=Route.active.filter(tourevent__in=TourEvent.objects.filter(tour__in=Tour.active.all())),
        label=_('Route')
    )
    #  проблемный код ------
    guide = django_filters.ModelMultipleChoiceFilter(
        queryset=GuideProfile.active.filter(tour__in=Tour.active.all()).distinct()
    )
    difficulty_level = django_filters.ModelMultipleChoiceFilter(
        queryset=DifficultyLevel.objects.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Difficulty Level')
    )
    physical_level = django_filters.ModelMultipleChoiceFilter(
        queryset=PhysicalLevel.objects.filter(tour__in=Tour.active.all()).distinct(),
        label=_('Physical Level')
    )
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label=_('Price min'))
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label=_('Price max'))

    #  разобраться с датами - теперь они в Calendar
    # from_date = django_filters.DateFilter(
    #     field_name='start_date',
    #     lookup_expr='gt',
    #     label=_('Date from'),
    #     widget=django.forms.DateInput(
    #         attrs={'type': 'date'}
    #     )
    # )
    # through_date = django_filters.DateFilter(
    #     field_name='end_date',
    #     lookup_expr='lt',
    #     label=_('Date through'),
    #     widget=django.forms.DateInput(
    #         attrs={'type': 'date'}
    #     )
    # )

    o = django_filters.OrderingFilter(
        fields=(
            #  разобраться с датами - теперь они в Calendar
            #  ('start_date', 'start_date'),
            #  ('end_date', 'end_date'),
            ('name', 'name'),
            ('price', 'price'),
            ('difficulty_level', 'difficulty_level'),
            ('physical_level', 'physical_level'),
        ),
        field_labels={
            'difficulty_level': 'Difficulty',
            'physical_level': 'Physical',
        }
    )

    class Meta:
        model = Tour
        fields = ['search', 'activity', 'continent', 'country', 'region',
                  'place', 'refuge', 'guide', 'price__gt', 'price__lt',
                  #  разобраться с этими полями - они ща в TourEvent
                  'tour_object', 'route',
                  #  разобраться с этими полями - они ща в Calendar
                  #  'from_date', 'through_date',
                  'difficulty_level', 'physical_level']

    def my_custom_filter(self, queryset, name, value):
        return Tour.objects.filter(
            Q(name__icontains=value) | Q(description__icontains=value) | Q(country__name__icontains=value) | Q(place__name__icontains=value)
            | Q(activity__name__icontains=value) | Q(region__name__icontains=value) | Q(continent__name__icontains=value)
            #  разобраться с этими полями - они сейчас с TourEvent
            | Q(tour_object__name__icontains=value) | Q(route__name__icontains=value)
            | Q(guide__name__icontains=value) | Q(refuge__name__icointains=value)
        ).distinct()
