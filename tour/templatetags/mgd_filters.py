from django import template

register = template.Library()


@register.filter(name='times')
def times(value):
    try:
        return range(1, value)
    except:
        return []

@register.filter(name='get_tour_object_route_filter')
def get_tour_object_route_filter(tour, tour_object):
    return tour.get_tour_object_route(tour_object)
