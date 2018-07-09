from collections import OrderedDict
from django.urls import reverse
import logging
from rest_framework.serializers import BaseSerializer

logger = logging.getLogger(__name__)

DEFAULT_LOCATION = [-23.5572, -46.7302]


class MapInfoSerializer(BaseSerializer):
    def to_representation(self, request):
        try:
            from django.contrib.gis.geoip2 import GeoIP2
            g = GeoIP2()
            location = list(g.lat_lon(request.META.get('REMOTE_ADDRESS', None)))
        except Exception as e:
            logger.warning("Couldn't get location (using default location instead): {}".format(str(e)))
            location = DEFAULT_LOCATION
        return OrderedDict({
            'cluster_url': reverse('api:cluster-list') + '?zoom_size={{zoom}}&in_bbox={{bbox}}=',
            'location': location
        })
