from base_station.viewsets import IdentifiedBaseStationViewSet
# from cluster.viewsets import ClusterViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'base_stations', IdentifiedBaseStationViewSet, base_name='base-station')
# router.register(r'cluster', ClusterViewSet, base_name='cluster')
