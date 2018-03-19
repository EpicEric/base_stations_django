from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
import logging

from base_station.models import IdentifiedBaseStation
from optimization.find_best_locations import find_best_locations

logger = logging.getLogger(__name__)

def index(request):
    try:
        from django.contrib.gis.geoip2 import GeoIP2
        g = GeoIP2()
        location = list(g.lat_lon(request.META.get('REMOTE_ADDRESS', None)))
    except Exception as e:
        logger.warning("[WARNING] Couldn't get location (using default location instead): {}".format(str(e)))
        location = [-23.5572, -46.7302]
    context = {'location': location}
    return render(request, 'base_station/index.html', context)

class ExampleView(TemplateView):
    template_name = 'base_station/example.html'
    
    def get(self, request, *args, **kwargs):
        location = [-46.7302, -23.5572]
        bounds = ((-46.74, -46.70), (-23.58, -23.55))

        bss = IdentifiedBaseStation.get_base_stations_inside_bounds(bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1])
        solution = find_best_locations(bss, 2, bounds)

        solution = [list(s) for s in solution]
        bs_coordinates = list(map(lambda bs: [bs.point.x, bs.point.y], bss))

        context = {'location': location, 'base_stations': bs_coordinates, 'suggestions': solution}
        return render(request, self.template_name, context)
