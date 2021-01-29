from django.urls import path
# from django_filters.views import FilterView
# from .filters import TourFilter

from . import views

app_name = 'tour'

urlpatterns = [
    path('', views.index, name='index'),
    path('participate/<int:pk>/', views.participate, name='participate'),
    path('site_statistics/', views.site_statistics, name='site_statistics'),
    path('tours/', views.TourFilterListView.as_view(), name='tour_list'),
    path('<slug:arg1>/', views.GlobalListView.as_view(), name="global-list"),
    path('<slug:arg1>/<slug:arg2>/<slug:arg3>/', views.ArgumentListView.as_view(), name="argument-list"),
    path('activity/<slug:slug>/', views.ActivityDetailView.as_view(), name='activity-detail'),
    path('continent/<slug:slug>/', views.ContinentDetailView.as_view(), name='continent-detail'),
    path('country/<slug:slug>/', views.CountryDetailView.as_view(), name='country-detail'),
    path('region/<slug:slug>/', views.RegionDetailView.as_view(), name='region-detail'),
    path('place/<slug:slug>/', views.PlaceDetailView.as_view(), name='place-detail'),
    path('guide/<slug:slug>/', views.GuideProfileDetailView.as_view(), name='guide-profile'),
    path('tour-object/<slug:slug>/', views.TourObjectDetailView.as_view(), name='tour-object-detail'),
    path('route/<slug:slug>/', views.RouteDetailView.as_view(), name='route-detail'),
    #  path('touring/<slug:slug>/', views.TouringDetailView.as_view(), name='touring-detail'),
    path('refuge/<slug:slug>/', views.RefugeDetailView.as_view(), name='refuge-detail'),
    path('tour/<slug:slug>/', views.TourDetailView.as_view(), name='tour-detail'),
]