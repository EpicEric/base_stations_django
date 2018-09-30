from django.shortcuts import render
from django.views.generic import TemplateView
import logging

from base_station.models import IdentifiedBaseStation
from optimization.find_best_locations import OptimizeLocation
from optimization.numerical_methods import Basinhopping, SLSQP, Taguchi
from optimization.propagation_models import (
    AreaOptimization, FreeSpacePathLossOptimization)

from .use_cases.heat_map import HeatMap

logger = logging.getLogger(__name__)


class OptimizationView(TemplateView):
    template_name = 'demo/optimization.html'


class ExampleView(TemplateView):
    template_name = 'demo/example.html'

    @staticmethod
    def get_bounds_from_parameters(request):
        min_lat = float(request.GET['min_lat'])
        max_lat = float(request.GET['max_lat'])
        min_long = float(request.GET['min_long'])
        max_long = float(request.GET['max_long'])

        return ((min_lat, max_lat), (min_long, max_long))


class BasinhoppingView(ExampleView):

    def get(self, request, *args, **kwargs):
        bounds = ExampleView.get_bounds_from_parameters(request)
        NUMBER_OF_NEW_BSS = 5
        bounds = bounds * NUMBER_OF_NEW_BSS

        location = [bounds[0][0] + (bounds[0][1] - bounds[0][0])/2,
                    bounds[1][0] + (bounds[1][1] - bounds[1][0])/2]
        bss = IdentifiedBaseStation.get_base_stations_inside_bounds(
            bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1])\
            .filter(radio='GSM')
        
        optimize = OptimizeLocation(bss, bounds, Basinhopping(), AreaOptimization().objective)
        solution = optimize.find_best_locations()
        solution = [list(s) for s in solution]
        bs_coordinates = list(map(lambda bs: [bs.point.x, bs.point.y], bss))
        context = {
            'location': location,
            'base_stations': bs_coordinates,
            'suggestions': solution}
        return render(request, self.template_name, context)


class SlsqpView(ExampleView):

    def get(self, request, *args, **kwargs):
        bounds = ExampleView.get_bounds_from_parameters(request)
        NUMBER_OF_NEW_BSS = 2
        bounds = bounds * NUMBER_OF_NEW_BSS

        location = [bounds[0][0] + (bounds[0][1] - bounds[0][0])/2,
                    bounds[1][0] + (bounds[1][1] - bounds[1][0])/2]
        bss = IdentifiedBaseStation.get_base_stations_inside_bounds(
            bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1])\
            .filter(radio='GSM')

        optimize = OptimizeLocation(bss, bounds, SLSQP(), AreaOptimization().objective)
        solution = optimize.find_best_locations()
        solution = [list(s) for s in solution]
        bs_coordinates = list(map(lambda bs: [bs.point.x, bs.point.y], bss))
        context = {
            'location': location,
            'base_stations': bs_coordinates,
            'suggestions': solution}
        return render(request, self.template_name, context)


class TaguchiView(ExampleView):

    def get(self, request, *args, **kwargs):
        bounds = ExampleView.get_bounds_from_parameters(request)
        NUMBER_OF_NEW_BSS = 2
        bounds = bounds * NUMBER_OF_NEW_BSS

        location = [bounds[0][0] + (bounds[0][1] - bounds[0][0])/2,
                    bounds[1][0] + (bounds[1][1] - bounds[1][0])/2]
        bss = IdentifiedBaseStation.get_base_stations_inside_bounds(
            bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1])\
            .filter(radio='GSM')

        optimize = OptimizeLocation(bss, bounds, Taguchi(), AreaOptimization().objective)
        solution = optimize.find_best_locations()
        solution = [list(s) for s in solution]
        bs_coordinates = list(map(lambda bs: [bs.point.x, bs.point.y], bss))
        context = {
            'location': location,
            'base_stations': bs_coordinates,
            'suggestions': solution}
        print(AreaOptimization().objective(bss, solution))
        return render(request, self.template_name, context)


class HeatMapView(TemplateView):
    template_name = 'demo/heat-map.html'

    def get(self, request, *args, **kwargs):
        location = [-46.7302, -23.5572]
        bounds = ExampleView.get_bounds_from_parameters(request)
        bss = IdentifiedBaseStation.get_base_stations_inside_bounds(
            bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1])\
            .filter(radio='GSM')
        heatMap = HeatMap(bss, bounds)
        bs_coordinates = list(map(lambda bs: [bs.point.x, bs.point.y], bss))

        context = {'location': location,
                   'base_stations': bs_coordinates,
                   'heatmap': heatMap.generate_heatmap()}
        return render(request, self.template_name, context)
