from rest_framework.viewsets import ModelViewSet
from rest_framework_gis.pagination import GeoJsonPagination

from .models import IdentifiedBaseStation
from .serializers import IdentifiedBaseStationSerializer


class BaseStationPagination(GeoJsonPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 300


class IdentifiedBaseStationViewSet(ModelViewSet):
    queryset = IdentifiedBaseStation.objects.all()
    serializer_class = IdentifiedBaseStationSerializer
    pagination_class = BaseStationPagination
