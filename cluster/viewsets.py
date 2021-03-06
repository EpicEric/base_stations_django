from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.filters import InBBoxFilter, DistanceToPointFilter
from rest_framework_gis.pagination import GeoJsonPagination

from base_station.models import Operator
from .models import BaseStationCluster, BS_MODEL, ZOOM_TO_GEOHASH_PRECISION, MAX_CLUSTER_ZOOM_SIZE
from .serializers import BaseStationClusterSerializer, BaseStationUnitSerializer


class BaseStationClusterPagination(GeoJsonPagination):
    page_size = 600
    page_size_query_param = 'page_size'
    max_page_size = 800


class BaseStationClusterViewSet(ReadOnlyModelViewSet):
    queryset = BaseStationCluster.objects.all().order_by('id')
    serializer_class = BaseStationClusterSerializer
    pagination_class = BaseStationClusterPagination
    bbox_filter_field = 'point'
    filter_backends = (InBBoxFilter, DistanceToPointFilter, DjangoFilterBackend)
    filter_fields = ('precision', 'operator')
    bbox_filter_include_overlapping = True

    def list(self, request, *args, **kwargs):
        query_params = request._request.GET.copy()
        zoom_size = query_params.pop('zoom_size', None)
        if not zoom_size:
            raise ParseError('Missing parameter \'zoom_size\'')
        if type(zoom_size) is list:
            zoom_size = zoom_size[0]
        try:
            zoom_size = int(zoom_size)
        except ValueError:
            raise ParseError('\'zoom_size\' must be an integer')

        # BaseStationCluster
        if zoom_size <= MAX_CLUSTER_ZOOM_SIZE:
            try:
                precision = ZOOM_TO_GEOHASH_PRECISION[int(zoom_size)]
                query_params['precision'] = precision
                operator_id = query_params.pop('operator', None)
                if operator_id and operator_id[0] and operator_id[0] != 'null':
                    operator = Operator.objects.get(id=operator_id[0])
                    self.queryset = self.queryset.filter(operator=operator)
                request._request.GET = query_params
            except KeyError:
                pass
            return super(BaseStationClusterViewSet, self).list(request, *args, **kwargs)

        # BS_MODEL
        return Response(BaseStationUnitViewSet.as_view({'get': 'list'})(request._request).data)
        # return BaseStationUnitViewSet(request=request, format=).list(request, *args, **kwargs)


class BaseStationUnitViewSet(ReadOnlyModelViewSet):
    queryset = BS_MODEL.objects.all().order_by('id')
    serializer_class = BaseStationUnitSerializer
    pagination_class = BaseStationClusterPagination
    bbox_filter_field = 'point'
    filter_backends = (InBBoxFilter, DistanceToPointFilter, DjangoFilterBackend)
    filter_fields = ()
    bbox_filter_include_overlapping = True

    def list(self, request, *args, **kwargs):
        query_params = request._request.GET.copy()
        operator_id = query_params.pop('operator', None)
        request._request.GET = query_params
        if operator_id and operator_id[0] and operator_id[0] != 'null':
            operator = Operator.objects.get(id=operator_id[0])
            mnc_list = [m.value for m in operator.mnc_set.all()]
            self.queryset = self.queryset.filter(mnc__in=mnc_list)
        return super(BaseStationUnitViewSet, self).list(request, *args, **kwargs)
