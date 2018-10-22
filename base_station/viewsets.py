from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.filters import InBBoxFilter, DistanceToPointFilter
from rest_framework_gis.pagination import GeoJsonPagination

from .models import IdentifiedBaseStation, Operator
from .serializers import IdentifiedBaseStationSerializer, OperatorSerializer


class BaseStationPagination(GeoJsonPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 300


class IdentifiedBaseStationViewSet(ReadOnlyModelViewSet):
    queryset = IdentifiedBaseStation.objects.all().order_by('id')
    serializer_class = IdentifiedBaseStationSerializer
    pagination_class = BaseStationPagination
    bbox_filter_field = 'point'
    filter_backends = (InBBoxFilter, DistanceToPointFilter, DjangoFilterBackend)
    filter_fields = ('radio',)
    bbox_filter_include_overlapping = True

class OperatorViewSet(ReadOnlyModelViewSet):
    queryset = Operator.objects.all().order_by('id')
    serializer_class = OperatorSerializer
