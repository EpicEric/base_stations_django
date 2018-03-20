from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
import logging

from base_station.models import IdentifiedBaseStation
from optimization.find_best_locations import find_best_locations, objective


import numpy as np
import itertools

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

class HeatMapView(TemplateView):
    template_name = 'base_station/heat-map.html'
    
    def get(self, request, *args, **kwargs):
        location = [-46.7302, -23.5572]
        bounds = ((-46.72, -46.71), (-23.57, -23.56))

        bss = IdentifiedBaseStation.get_base_stations_inside_bounds(bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1]).filter(radio='GSM')


        x = np.linspace(bounds[0][0], bounds[0][1], num=70)
        y = np.linspace(bounds[1][0], bounds[1][1], num=70)
        coord = [list(e) for e in itertools.product(x,y)]

        covered_area_by_bs = list(map(lambda bs: bs.covered_area, bss))
        heatmap = list(map(lambda coord: [coord[1], coord[0], (-objective(covered_area_by_bs, coord))*110*110, ], coord))
        heatmap = sorted(heatmap, key=lambda x: x[2])
        threshold = heatmap[-1][2]*(10/100)
        print(heatmap[-1][2])
        print(heatmap[0][2])


        print(heatmap[-1][2]-heatmap[0][2])
        print(threshold)
        filtered_heatmap = list(filter(lambda x: heatmap[-1][2] - x[2] <= threshold, heatmap))
        bs_coordinates = list(map(lambda bs: [bs.point.x, bs.point.y], bss))

        context = {'location': location, 'base_stations': bs_coordinates, 'heatmap': filtered_heatmap}
        return render(request, self.template_name, context)
