from .models import Tour, Activity, Continent, Country, Region,\
    Place, TourObject, Route, Touring, GuideProfile
import django_filters

class TourFilter(django_filters.FilterSet):
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
    class Meta:
        model = Tour
        fields = ['activity', 'continent', 'country', 'region',
                  'place', 'tour_object', 'route', 'touring', 'guide']
