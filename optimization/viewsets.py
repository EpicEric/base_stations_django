from rest_framework import viewsets
from rest_framework.response import Response
from .find_best_locations import OptimizeLocation
from base_station.models import IdentifiedBaseStation

class OptimizationViewSet(viewsets.ViewSet):
    def list(self, request):
        query_params = request._request.GET.copy()
        min_lat = float(query_params.pop('min_lat', None)[0])
        max_lat = float(query_params.pop('max_lat', None)[0])
        min_long = float(query_params.pop('min_long', None)[0])
        max_long = float(query_params.pop('max_long', None)[0])

        bounds = ((min_lat, max_lat), (min_long, max_long))
        bss = IdentifiedBaseStation.get_base_stations_inside_bounds(
            bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1])\
            .filter(radio='GSM')
        solution = OptimizeLocation.taguchi(bss, 2, bounds)

        solution = [list(s) for s in solution]
        bs_coordinates = list(map(lambda bs: [bs.point.x, bs.point.y], bss))

        response = {'suggestions': solution}
        return Response(response)

