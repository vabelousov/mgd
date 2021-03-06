from mgd.settings import EMAIL_HOST_USER
from . import forms
from django.db.models import Min
from django.core.mail import send_mail
from json import dumps
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView
from .filters import CalendarFilter
from .models import Activity, Continent, Country,\
    Region, Place, TourObject, Route, Tour, Refuge,\
    GuideProfile, TourEvent, Calendar


def participate(request, pk):
    par = forms.Participate()
    if request.method == 'POST':
        par = forms.Participate(request.POST)
        subject = 'Participation request'
        message = 'Please contact me for this participation request, tour id:'+str(pk)
        recepient = str(par['e_mail'].value())
        send_mail(subject,
            message, recepient, [EMAIL_HOST_USER], fail_silently=False)
        return render(request, 'email_success.html', {'recepient': 'site admin'})
    return render(request, 'email_participate.html', {'form': par, 'tour': Calendar.objects.get(pk=pk)})


def index(request):
    dict_values = Calendar.active.order_by('tour').values('tour__pk').annotate(Min('start_date'))[:4]
    list_of_ids = []
    for v in dict_values:
        list_of_ids.append(Calendar.active.get(tour__pk__exact=v['tour__pk'], start_date__exact=v['start_date__min']).pk)
    objects = Calendar.objects.filter(pk__in=list_of_ids)
    return render(
        request,
        'index.html',
        context={
            'object_list': objects,
            'activity_list': Activity.active.all(),
            'continent_list': Continent.active.all(),
            'country_list': Country.active.all(),
            'region_list': Region.active.all(),
            'place_list': Place.active.all(),
            'route_list': Route.active.all(),
            'refuge_list': Refuge.active.all()
        },
    )


def site_statistics(request):
    activities = Activity.active.count()
    continents = Continent.active.count()
    countries = Country.active.count()
    regions = Region.active.count()
    places = Place.active.count()
    tour_objects = TourObject.active.count()
    routes = Route.active.count()
    refuges = Refuge.active.count()
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
                 'refuges': refuges,
                 'tours': tours,
                 'guides': guides,
        },
    )


class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context


class TourFilterListView(FilteredListView):
    model = Calendar
    paginate_by = 6
    context_object_name = 'tour_list'
    template_name = 'tour_list.html'
    filterset_class = CalendarFilter


class GlobalListView(ListView):
    paginate_by = 12
    context_object_name = 'objects'
    template_name = 'global_list.html'

    def get_queryset(self):
        objects = Tour.active.all()
        if self.kwargs['arg1'] == 'activities':
            objects = Activity.active.all()
        if self.kwargs['arg1'] == 'guides':
            objects = GuideProfile.active.all()
        if self.kwargs['arg1'] == 'continents':
            objects = Continent.active.all()
        if self.kwargs['arg1'] == 'countries':
            objects = Country.active.all()
        if self.kwargs['arg1'] == 'regions':
            objects = Region.active.all()
        if self.kwargs['arg1'] == 'places':
            objects = Place.active.all()
        if self.kwargs['arg1'] == 'tour-objects':
            objects = TourObject.active.all()
        if self.kwargs['arg1'] == 'routes':
            objects = Route.active.all()
        if self.kwargs['arg1'] == 'refuges':
            objects = Refuge.active.all()
        return objects

    def get_context_data(self, **kwargs):
        context = super(GlobalListView, self).get_context_data(**kwargs)
        context['list_title'] = _(self.kwargs['arg1'])
        return context


class ArgumentListView(ListView):
    paginate_by = 5
    context_object_name = 'objects'
    template_name = 'global_list.html'

    def get_queryset(self):
        objects = Tour.active.all()
        if self.kwargs['arg3'] == 'activities':
            routes = None
            if self.kwargs['arg1'] == 'continent':
                routes = Route.active.filter(
                    tourevent__route__place__region__country__continent__slug=self.kwargs['arg2']
                )
            if self.kwargs['arg1'] == 'country':
                routes = Route.active.filter(tourevent__route__place__region__country__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'region':
                routes = Route.active.filter(tourevent__route__place__region__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'place':
                routes = Route.active.filter(tourevent__route__place__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'guide':
                routes = Route.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        tour__in=Tour.active.filter(guide__slug=self.kwargs['arg2'])
                    )
                )
            if self.kwargs['arg1'] == 'refuge':
                routes = Route.active.filter(tourevent__route__refuge__slug=self.kwargs['arg2'])
            objects = Activity.active.filter(route__in=routes).distinct()
        if self.kwargs['arg3'] == 'continents':
            countries = None
            if self.kwargs['arg1'] == 'activity':
                countries = Country.active.filter(
                    region__in=Region.active.filter(
                        place__in=Place.active.filter(
                            route__in=Route.active.filter(activity__slug__exact=self.kwargs['arg2'])
                        )
                    )
                )
            if self.kwargs['arg1'] == 'guide':
                countries = Country.active.filter(
                    region__in=Region.active.filter(
                        place__in=Place.active.filter(
                            route__in=Route.active.filter(
                                tourevent__in=TourEvent.objects.filter(
                                    tour__in=Tour.active.filter(guide__slug=self.kwargs['arg2'])
                                )
                            )
                        )
                    )
                )
            objects = Continent.active.filter(country__in=countries).distinct()
        if self.kwargs['arg3'] == 'countries':
            regions = None
            if self.kwargs['arg1'] == 'activity':
                regions = Region.active.filter(
                    place__in=Place.active.filter(
                        route__in=Route.active.filter(activity__slug__exact=self.kwargs['arg2'])
                    )
                )
            if self.kwargs['arg1'] == 'continent':
                return Country.active.filter(continent__slug__exact=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'guide':
                regions = Region.active.filter(
                    place__in=Place.active.filter(
                        route__in=Route.active.filter(
                            tourevent__in=TourEvent.objects.filter(
                                tour__in=Tour.active.filter(guide__slug=self.kwargs['arg2'])
                            )
                        )
                    )
                )
            objects = Country.active.filter(region__in=regions).distinct()
        if self.kwargs['arg3'] == 'regions':
            places = None
            if self.kwargs['arg1'] == 'activity':
                places = Place.active.filter(
                    route__in=Route.active.filter(activity__slug__exact=self.kwargs['arg2'])
                )
            if self.kwargs['arg1'] == 'continent':
                places = Place.active.filter(region__country__continent__slug__exact=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'country':
                places = Place.active.filter(region__country__slug__exact=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'guide':
                places = Place.active.filter(
                    route__in=Route.active.filter(
                        tourevent__in=TourEvent.objects.filter(
                            tour__in=Tour.active.filter(guide__slug=self.kwargs['arg2'])
                        )
                    )
                )
            objects = Region.active.filter(place__in=places).distinct()
        if self.kwargs['arg3'] == 'places':
            routes = None
            if self.kwargs['arg1'] == 'activity':
                routes = Route.active.filter(activity__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'continent':
                routes = Route.active.filter(place__region__country__continent__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'country':
                routes = Route.active.filter(place__region__country__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'region':
                routes = Route.active.filter(place__region__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'guide':
                routes = Route.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        tour__in=Tour.active.filter(guide__slug=self.kwargs['arg2'])
                   )
                )
            if self.kwargs['arg1'] == 'tour-object':
                routes = Route.active.filter(tour_object__slug__exact=self.kwargs['arg2'])
            objects = Place.active.filter(route__in=routes).distinct()
        if self.kwargs['arg3'] == 'refuges':
            routes = None
            if self.kwargs['arg1'] == 'activity':
                routes = Route.active.filter(activity__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'continent':
                routes = Route.active.filter(place__region__country__continent__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'country':
                routes = Route.active.filter(place__region__country__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'region':
                routes = Route.active.filter(place__region__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'place':
                routes = Route.active.filter(place__slug=self.kwargs['arg2'])
            if self.kwargs['arg1'] == 'tour-object':
                routes = Route.active.filter(tour_object__slug__exact=self.kwargs['arg2'])
            objects = Refuge.active.filter(route__in=routes).distinct()
        if self.kwargs['arg3'] == 'tour-objects':
            if self.kwargs['arg1'] == 'guide':
                guide_tours = Tour.active.filter(guide__slug=self.kwargs['arg2'])
                tour_events = TourEvent.objects.filter(tour__in=guide_tours)
                objects = TourObject.active.filter(tourevent__in=tour_events).distinct()
            if self.kwargs['arg1'] == 'activity':
                objects = TourObject.active.filter(
                    route__in=Route.active.filter(activity__slug__exact=self.kwargs['arg2'])
                ).distinct()
            if self.kwargs['arg1'] == 'refuge':
                objects = TourObject.active.filter(
                    route__in=Route.active.filter(refuge__slug__exact=self.kwargs['arg2'])
                ).distinct()
            if self.kwargs['arg1'] == 'continent':
                countries = Country.active.filter(continent__slug=self.kwargs['arg2'])
                regions = Region.active.filter(country__in=countries)
                places = Place.active.filter(region__in=regions)
                routes = Route.active.filter(place__in=places)
                objects = TourObject.active.filter(route__in=routes).distinct()
            if self.kwargs['arg1'] == 'country':
                regions = Region.active.filter(country__slug=self.kwargs['arg2'])
                places = Place.active.filter(region__in=regions)
                routes = Route.active.filter(place__in=places)
                objects = TourObject.active.filter(route__in=routes).distinct()
            if self.kwargs['arg1'] == 'region':
                places = Place.active.filter(region__slug=self.kwargs['arg2'])
                routes = Route.active.filter(place__in=places)
                objects = TourObject.active.filter(route__in=routes).distinct()
            if self.kwargs['arg1'] == 'place':
                routes = Route.active.filter(place__slug=self.kwargs['arg2'])
                objects = TourObject.active.filter(route__in=routes).distinct()
        if self.kwargs['arg3'] == 'routes':
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
            if self.kwargs['arg1'] == 'guide':
                guide_tours = Tour.active.filter(guide__slug=self.kwargs['arg2'])
                tour_events = TourEvent.objects.filter(tour__in=guide_tours)
                objects = Route.active.filter(tourevent__in=tour_events).distinct()
            if self.kwargs['arg1'] == 'refuge':
                objects = Route.active.filter(refuge__slug__exact=self.kwargs['arg2']).distinct()
            if self.kwargs['arg1'] == 'activity':
                objects = Route.active.filter(activity__slug__exact=self.kwargs['arg2']).distinct()
        if self.kwargs['arg3'] == 'tours':
            if self.kwargs['arg1'] == 'activity':
                objects = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        route__in=Route.active.filter(activity__slug__exact=self.kwargs['arg2'])
                    )
                ).distinct()
            if self.kwargs['arg1'] == 'guide':
                objects = Tour.active.filter(guide__slug=self.kwargs['arg2']).all()
            if self.kwargs['arg1'] == 'continent':
                objects = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        route__in=Route.active.filter(
                            place__in=Place.active.filter(
                                region__in=Region.active.filter(
                                    country__in=Country.active.filter(continent__slug__exact=self.kwargs['arg2'])
                                )
                            )
                        )
                    )
                ).distinct()
            if self.kwargs['arg1'] == 'country':
                objects = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        route__in=Route.active.filter(
                            place__in=Place.active.filter(
                                region__in=Region.active.filter(country__slug__exact=self.kwargs['arg2'])
                            )
                        )
                    )
                ).distinct()
            if self.kwargs['arg1'] == 'region':
                objects = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        route__in=Route.active.filter(
                            place__in=Place.active.filter(region__slug__exact=self.kwargs['arg2'])
                        )
                    )
                ).distinct()
            if self.kwargs['arg1'] == 'place':
                objects = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        route__in=Route.active.filter(place__slug__exact=self.kwargs['arg2'])
                    )
                ).distinct()
            if self.kwargs['arg1'] == 'tour-object':
                objects = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(tour_object__slug=self.kwargs['arg2'])
                ).distinct()
            if self.kwargs['arg1'] == 'route':
                objects = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(route__slug=self.kwargs['arg2'])
                ).distinct()
            if self.kwargs['arg1'] == 'refuge':
                objects = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        route__in=Route.active.filter(refuge__slug=self.kwargs['arg2'])
                    )
                ).distinct()
        if self.kwargs['arg3'] == 'guides':
            tours = None
            if self.kwargs['arg1'] == 'activity':
                tours = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        route__in=Route.active.filter(activity__slug__exact=self.kwargs['arg2'])
                    )
                )
            if self.kwargs['arg1'] == 'continent':
                tours = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        route__in=Route.active.filter(
                            place__in=Place.active.filter(
                                region__in=Region.active.filter(
                                    country__in=Country.active.filter(continent__slug__exact=self.kwargs['arg2'])
                                )
                            )
                        )
                    )
                )
            if self.kwargs['arg1'] == 'country':
                tours = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        route__in=Route.active.filter(
                            place__in=Place.active.filter(
                                region__in=Region.active.filter(country__slug__exact=self.kwargs['arg2'])
                            )
                        )
                    )
                )
            if self.kwargs['arg1'] == 'region':
                tours = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        route__in=Route.active.filter(
                            place__in=Place.active.filter(region__slug__exact=self.kwargs['arg2'])
                        )
                    )
                )
            if self.kwargs['arg1'] == 'place':
                tours = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        route__in=Route.active.filter(place__slug__exact=self.kwargs['arg2'])
                    )
                )
            if self.kwargs['arg1'] == 'tour-object':
                tours = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(tour_object__slug=self.kwargs['arg2'])
                ).distinct()
            if self.kwargs['arg1'] == 'route':
                tours = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(route__slug=self.kwargs['arg2'])
                ).distinct()
            if self.kwargs['arg1'] == 'refuge':
                tours = Tour.active.filter(
                    tourevent__in=TourEvent.objects.filter(
                        route__in=Route.active.filter(refuge__slug__exact=self.kwargs['arg2'])
                    )
                )
            objects = GuideProfile.active.filter(tour__in=tours).distinct()
        return objects

    def get_context_data(self, **kwargs):
        context = super(ArgumentListView, self).get_context_data(**kwargs)
        context['list_title'] = _(self.kwargs['arg3'])
        return context


class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'global_detail.html'

    def get_success_url(self):
        return reverse('tour:activity-detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(ActivityDetailView, self).get_context_data(**kwargs)
        context['type'] = 'activity'
        return context


class ContinentDetailView(DetailView):
    model = Continent
    template_name = 'global_detail.html'

    def get_success_url(self):
        return reverse('tour:continent-detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(ContinentDetailView, self).get_context_data(**kwargs)
        context['type'] = 'continent'
        return context


class CountryDetailView(DetailView):
    model = Country
    template_name = 'global_detail.html'

    def get_success_url(self):
        return reverse('tour:country-detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(CountryDetailView, self).get_context_data(**kwargs)
        context['type'] = 'country'
        return context


class RegionDetailView(DetailView):
    model = Region
    template_name = 'global_detail.html'

    def get_success_url(self):
        return reverse('tour:region-detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(RegionDetailView, self).get_context_data(**kwargs)
        context['type'] = 'region'
        return context


class PlaceDetailView(DetailView):
    model = Place
    template_name = 'global_detail.html'

    def get_success_url(self):
        return reverse('tour:place-detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(PlaceDetailView, self).get_context_data(**kwargs)
        context['type'] = 'place'
        return context


class TourObjectDetailView(DetailView):
    model = TourObject
    template_name = 'global_detail.html'

    def get_success_url(self):
        return reverse('tour:tour-object-detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(TourObjectDetailView, self).get_context_data(**kwargs)
        context['type'] = 'tour-object'
        return context


class RouteDetailView(DetailView):
    model = Route
    template_name = 'global_detail.html'

    def get_success_url(self):
        return reverse('tour:route-detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(RouteDetailView, self).get_context_data(**kwargs)
        context['type'] = 'route'
        return context


class RefugeDetailView(DetailView):
    model = Refuge
    template_name = 'global_detail.html'

    def get_success_url(self):
        return reverse('tour:refuge-detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(RefugeDetailView, self).get_context_data(**kwargs)
        context['type'] = 'refuge'
        return context


class TourDetailView(DetailView):
    model = Tour
    template_name = 'tour_detail.html'

    def get_success_url(self):
        return reverse('tour:tour-detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(TourDetailView, self).get_context_data(**kwargs)
        obj = context['object']
        alti_data = obj.get_alti_data_plot()
        days_data = obj.get_days_data_plot()
        dataDictionary = {'altitude': alti_data, 'days': days_data}
        dataJSON = dumps(dataDictionary)
        context['data'] = dataJSON
        return context


class GuideProfileDetailView(DetailView):
    model = GuideProfile
    template_name = 'global_detail.html'

    def get_success_url(self):
        return reverse('tour:guide-detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(GuideProfileDetailView, self).get_context_data(**kwargs)
        context['type'] = 'guide'
        return context