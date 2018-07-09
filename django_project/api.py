from rest_framework import routers

# from base_station.viewsets import IdentifiedBaseStationViewSet
from cluster.viewsets import BaseStationClusterViewSet
from map.viewsets import MapInfoViewSet


router = routers.DefaultRouter()
# router.register(r'base_station', IdentifiedBaseStationViewSet, base_name='base-station')
router.register(r'cluster', BaseStationClusterViewSet, base_name='cluster')
router.register(r'map_info', MapInfoViewSet, base_name='map_info')
