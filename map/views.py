from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import logging

from cluster.models import MAX_CLUSTER_ZOOM_SIZE

logger = logging.getLogger(__name__)


@login_required
def index(request):
    try:
        from django.contrib.gis.geoip2 import GeoIP2
        g = GeoIP2()
        location = list(g.lat_lon(request.META.get('REMOTE_ADDRESS', None)))
    except Exception as e:
        logger.warning("Couldn't get location (using default location instead): {}".format(str(e)))
        location = [-23.5572, -46.7302]
    context = {'location': location, 'max_zoom': MAX_CLUSTER_ZOOM_SIZE}
    return render(request, 'map/index.html', context)
