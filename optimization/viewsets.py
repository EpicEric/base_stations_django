from rest_framework import viewsets
from rest_framework.response import Response
from .find_best_locations import OptimizeLocation
from base_station.models import IdentifiedBaseStation
from .util import distance

class OptimizationViewSet(viewsets.ViewSet):
    def list(self, request):
        query_params = request._request.GET.copy()

        min_lat = float(query_params.pop('min_lat', None)[0])
        max_lat = float(query_params.pop('max_lat', None)[0])
        min_long = float(query_params.pop('min_long', None)[0])
        max_long = float(query_params.pop('max_long', None)[0])
        number_erbs = query_params.pop('number_erbs', None)
        if number_erbs:
            number_erbs = int(number_erbs[0])
        else:
            number_erbs = 1

        bounds = ((min_lat, max_lat), (min_long, max_long))
        bss = IdentifiedBaseStation.get_base_stations_inside_bounds(
            bounds[1][0] - 1/220, bounds[0][0] - 1/220, bounds[1][1] + 1/220, bounds[0][1] + 1/220)\
            .filter(radio='GSM')

        result_random = OptimizeLocation.random_search(bss, number_erbs, bounds, 100)
        result = OptimizeLocation.taguchi(bss, number_erbs, bounds)

        suggestions = [list(s) for s in result[0]]
        area = result[1]
        response = {'suggestions': suggestions, "areaTaguchi": area, "areaRandom": result_random[1]}
        if number_erbs == 2:
            if distance(suggestions[0], suggestions[1]) <= 1/440:
                response['message'] = 'Instalar uma antena só é a melhor opção.'

        return Response(response)
