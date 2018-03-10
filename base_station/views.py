from django.shortcuts import render
import logging


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
