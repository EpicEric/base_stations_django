from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.filters import InBBoxFilter, DistanceToPointFilter
from rest_framework_gis.pagination import GeoJsonPagination

from .models import BaseStationCluster, ZOOM_TO_GEOHASH_PRECISION
from .serializers import BaseStationClusterSerializer


class BaseStationClusterPagination(GeoJsonPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 300


class BaseStationClusterViewSet(ReadOnlyModelViewSet):
    queryset = BaseStationCluster.objects.all().order_by('id')
    serializer_class = BaseStationClusterSerializer
    pagination_class = BaseStationClusterPagination
    bbox_filter_field = 'point'
    filter_backends = (InBBoxFilter, DistanceToPointFilter, DjangoFilterBackend)
    filter_fields = ('precision',)
    bbox_filter_include_overlapping = True

    def list(self, request, *args, **kwargs):
        query_params = request._request.GET.copy()
        zoom_size = query_params.pop('zoom_size', None)
        if zoom_size:
            try:
                if type(zoom_size) is list:
                    zoom_size = zoom_size[0]
                precision = ZOOM_TO_GEOHASH_PRECISION[int(zoom_size)]
                query_params['precision'] = precision
                request._request.GET = query_params
            except KeyError:
                pass
        return super(BaseStationClusterViewSet, self).list(request, *args, **kwargs)
