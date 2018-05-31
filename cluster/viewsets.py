from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework_gis.filters import InBBoxFilter, DistanceToPointFilter
from rest_framework_gis.pagination import GeoJsonPagination

from .models import BaseStationCluster
from .serializers import BaseStationClusterSerializer


class BaseStationClusterPagination(GeoJsonPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 300


class BaseStationClusterViewSet(ModelViewSet):
    queryset = BaseStationCluster.objects.all().order_by('id')
    serializer_class = BaseStationClusterSerializer
    pagination_class = BaseStationClusterPagination
    bbox_filter_field = 'point'
    filter_backends = (InBBoxFilter, DistanceToPointFilter, DjangoFilterBackend)
    filter_fields = ('zoom_size',)
    bbox_filter_include_overlapping = True

