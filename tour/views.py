from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView
from .models import Activity, Continent, Country,\
    Region, Place, TourObject, Route, Touring, Tour,\
    GuideProfile

# Create your views here.

def index(request):
    return render(
        request,
        'index.html',
        context={},
    )


def site_statistics(request):
    activities = Activity.active.count()
    continents = Continent.active.count()
    countries = Country.active.count()
    regions = Region.active.count()
    places = Place.active.count()
    tour_objects = TourObject.active.count()
    routes = Route.active.count()
    tourings = Touring.active.count()
    guides = GuideProfile.active.count()
    tours = Tour.active.count()
    return render(
        request,
        'site_statistics.html',
        context={'activities': activities,
                 'continents': continents,
                 'countries': countries,
                 'regions': regions,
                 'places': places,
                 'tour_objects': tour_objects,
                 'routes': routes,
                 'tourings': tourings,
                 'tours': tours,
                 'guides': guides,
        },
    )


class GlobalListView(ListView):
    paginate_by = 20
    context_object_name = 'objects'
    template_name = 'global_list.html'

    def get_queryset(self):
        objects = Tour.active.all()
        if self.kwargs['arg1'] == 'activities':
            self.template_name = 'activity_list.html'
            objects = Activity.active.all()
        if self.kwargs['arg1'] == 'guides':
            self.template_name = 'guide_list.html'
            objects = GuideProfile.active.all()
        if self.kwargs['arg1'] == 'continents':
            self.template_name = 'continent_list.html'
            objects = Continent.active.all()
        if self.kwargs['arg1'] == 'countries':
            self.template_name = 'country_list.html'
            objects = Country.active.all()
        if self.kwargs['arg1'] == 'regions':
            self.template_name = 'region_list.html'
            objects = Region.active.all()
        if self.kwargs['arg1'] == 'places':
            self.template_name = 'place_list.html'
            objects = Place.active.all()
        if self.kwargs['arg1'] == 'tour-objects':
            self.template_name = 'tour_object_list.html'
            objects = TourObject.active.all()
        if self.kwargs['arg1'] == 'routes':
            self.template_name = 'route_list.html'
            objects = Route.active.all()
        if self.kwargs['arg1'] == 'tourings':
            self.template_name = 'touring_list.html'
            objects = Touring.active.all()
        return objects


class ArgumentListView(ListView):
    paginate_by = 20
    context_object_name = 'objects'
    template_name = 'global_list.html'

    def get_queryset(self):
        objects = Tour.active.all()
        if self.kwargs['arg3'] == 'activities':
            self.template_name = 'activity_list.html'
            tours = None
            if self.kwargs['arg1'] == 'continent':
                tours = Tour.active.filter(continent__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'country':
                tours = Tour.active.filter(country__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'region':
                tours = Tour.active.filter(region__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'place':
                tours = Tour.active.filter(place__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'guide':
                tours = Tour.active.filter(guide__slug=self.kwargs['arg2'])
            objects = Activity.active.filter(tour__in=tours).distinct()
        if self.kwargs['arg3'] == 'continents':
            self.template_name = 'continent_list.html'
            tours = None
            if self.kwargs['arg1'] == 'activity':
                tours = Tour.active.filter(activity__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'country':
                tours = Tour.active.filter(country__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'region':
                tours = Tour.active.filter(region__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'place':
                tours = Tour.active.filter(place__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'guide':
                tours = Tour.active.filter(guide__slug=self.kwargs['arg2'])
            objects = Continent.active.filter(tour__in=tours).distinct()
        if self.kwargs['arg3'] == 'countries':
            self.template_name = 'country_list.html'
            tours = None
            if self.kwargs['arg1'] == 'activity':
                tours = Tour.active.filter(activity__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'continent':
                tours = Tour.active.filter(continent__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'region':
                tours = Tour.active.filter(region__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'place':
                tours = Tour.active.filter(place__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'guide':
                tours = Tour.active.filter(guide__slug=self.kwargs['arg2'])
            objects = Country.active.filter(tour__in=tours).distinct()
        if self.kwargs['arg3'] == 'regions':
            self.template_name = 'region_list.html'
            tours = None
            if self.kwargs['arg1'] == 'activity':
                tours = Tour.active.filter(activity__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'continent':
                tours = Tour.active.filter(continent__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'country':
                tours = Tour.active.filter(country__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'place':
                tours = Tour.active.filter(place__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'guide':
                tours = Tour.active.filter(guide__slug=self.kwargs['arg2'])
            objects = Region.active.filter(tour__in=tours).distinct()
        if self.kwargs['arg3'] == 'places':
            self.template_name = 'place_list.html'
            tours = None
            if self.kwargs['arg1'] == 'activity':
                tours = Tour.active.filter(activity__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'continent':
                tours = Tour.active.filter(continent__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'country':
                tours = Tour.active.filter(country__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'region':
                tours = Tour.active.filter(region__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'guide':
                tours = Tour.active.filter(guide__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'tour-object':
                tours = Tour.active.filter(tour_object__slug=self.kwargs['arg2'])
            objects = Place.active.filter(tour__in=tours).distinct()
        if self.kwargs['arg3'] == 'tour-objects':
            self.template_name = 'tour_object_list.html'
            if self.kwargs['arg1'] == 'guide':
                guide_tours = Tour.active.filter(guide__slug=self.kwargs['arg2'])
                objects = TourObject.active.filter(tour__in=guide_tours).distinct()
            if self.kwargs['arg1'] == 'continent':
                countries = Country.active.filter(continent__slug=self.kwargs['arg2'])
                regions = Region.active.filter(country__in=countries)
                places = Place.active.filter(region__in=regions)
                objects = TourObject.active.filter(place__in=places).distinct()
            if self.kwargs['arg1'] == 'country':
                regions = Region.active.filter(country__slug=self.kwargs['arg2'])
                places = Place.active.filter(region__in=regions)
                objects = TourObject.active.filter(place__in=places).distinct()
            if self.kwargs['arg1'] == 'region':
                places = Place.active.filter(region__slug=self.kwargs['arg2'])
                objects = TourObject.active.filter(place__in=places).distinct()
            if self.kwargs['arg1'] == 'place':
                objects = TourObject.active.filter(place__slug=self.kwargs['arg2']).distinct()
        if self.kwargs['arg3'] == 'routes':
            self.template_name = 'route_list.html'
            if self.kwargs['arg1'] == 'continent':
                countries = Country.active.filter(continent__slug=self.kwargs['arg2'])
                regions = Region.active.filter(country__in=countries)
                places = Place.active.filter(region__in=regions)
                objects = Route.active.filter(place__in=places)
            if self.kwargs['arg1'] == 'country':
                regions = Region.active.filter(country__slug=self.kwargs['arg2'])
                places = Place.active.filter(region__in=regions)
                objects = Route.active.filter(place__in=places)
            if self.kwargs['arg1'] == 'region':
                places = Place.active.filter(region__slug=self.kwargs['arg2'])
                objects = Route.active.filter(place__in=places)
            if self.kwargs['arg1'] == 'place':
                objects = Route.active.filter(place__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'tour-object':
                objects = Route.active.filter(tour_object__slug=self.kwargs['arg2'])
        if self.kwargs['arg3'] == 'tourings':
            self.template_name = 'touring_list.html'
            if self.kwargs['arg1'] == 'continent':
                countries = Country.active.filter(continent__slug=self.kwargs['arg2'])
                regions = Region.active.filter(country__in=countries)
                places = Place.active.filter(region__in=regions)
                objects = Touring.active.filter(place__in=places)
            if self.kwargs['arg1'] == 'country':
                regions = Region.active.filter(country__slug=self.kwargs['arg2'])
                places = Place.active.filter(region__in=regions)
                objects = Touring.active.filter(place__in=places)
            if self.kwargs['arg1'] == 'region':
                places = Place.active.filter(region__slug=self.kwargs['arg2'])
                objects = Touring.active.filter(place__in=places)
            if self.kwargs['arg1'] == 'place':
                objects = Touring.active.filter(place__slug=self.kwargs['arg2'])
        if self.kwargs['arg3'] == 'tours':
            self.template_name = 'no_filter_tour_list.html'
            if self.kwargs['arg1'] == 'activity':
                objects = Tour.active.filter(activity__slug=self.kwargs['arg2']).all()
            if self.kwargs['arg1'] == 'guide':
                objects = Tour.active.filter(guide__slug=self.kwargs['arg2']).all()
            if self.kwargs['arg1'] == 'continent':
                objects = Tour.active.filter(continent__slug=self.kwargs['arg2']).distinct()
            if self.kwargs['arg1'] == 'country':
                objects = Tour.active.filter(country__slug=self.kwargs['arg2']).distinct()
            if self.kwargs['arg1'] == 'region':
                objects = Tour.active.filter(region__slug=self.kwargs['arg2']).distinct()
            if self.kwargs['arg1'] == 'place':
                objects = Tour.active.filter(place__slug=self.kwargs['arg2']).distinct()
            if self.kwargs['arg1'] == 'tour-object':
                objects = Tour.active.filter(tour_object__slug=self.kwargs['arg2'])
        if self.kwargs['arg3'] == 'guides':
            self.template_name = 'guide_list.html'
            tours = None
            if self.kwargs['arg1'] == 'activity':
                tours = Tour.active.filter(activity__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'continent':
                tours = Tour.active.filter(continent__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'country':
                tours = Tour.active.filter(country__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'region':
                tours = Tour.active.filter(region__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'place':
                tours = Tour.active.filter(place__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'tour-object':
                tours = Tour.active.filter(tour_object__slug=self.kwargs['arg2'])
            objects = GuideProfile.active.filter(tour__in=tours).distinct()
        return objects


class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activity_detail.html'

    def get_success_url(self):
        return reverse('tour:activity-detail', kwargs={'slug': self.kwargs['slug']})


class ContinentDetailView(DetailView):
    model = Continent
    template_name = 'continent_detail.html'

    def get_success_url(self):
        return reverse('tour:continent-detail', kwargs={'slug': self.kwargs['slug']})


class CountryDetailView(DetailView):
    model = Country
    template_name = 'country_detail.html'

    def get_success_url(self):
        return reverse('tour:country-detail', kwargs={'slug': self.kwargs['slug']})


class RegionDetailView(DetailView):
    model = Region
    template_name = 'region_detail.html'

    def get_success_url(self):
        return reverse('tour:region-detail', kwargs={'slug': self.kwargs['slug']})


class TourObjectDetailView(DetailView):
    model = TourObject
    template_name = 'tour_object_detail.html'

    def get_success_url(self):
        return reverse('tour:tour-object-detail', kwargs={'slug': self.kwargs['slug']})


class RouteDetailView(DetailView):
    model = Route
    template_name = 'route_detail.html'

    def get_success_url(self):
        return reverse('tour:route-detail', kwargs={'slug': self.kwargs['slug']})


class PlaceDetailView(DetailView):
    model = Place
    template_name = 'place_detail.html'

    def get_success_url(self):
        return reverse('tour:place-detail', kwargs={'slug': self.kwargs['slug']})


class TouringDetailView(DetailView):
    model = Touring
    template_name = 'touring_detail.html'

    def get_success_url(self):
        return reverse('tour:touring-detail', kwargs={'slug': self.kwargs['slug']})


class TourDetailView(DetailView):
    model = Tour
    template_name = 'tour_detail.html'

    def get_success_url(self):
        return reverse('tour:tour-detail', kwargs={'slug': self.kwargs['slug']})


class GuideProfileDetailView(DetailView):
    model = GuideProfile
    template_name = 'guide_profile.html'

    def get_success_url(self):
        return reverse('tour:guide-detail', kwargs={'slug': self.kwargs['slug']})
