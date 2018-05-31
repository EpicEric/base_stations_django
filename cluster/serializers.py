from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import BaseStationCluster


class BaseStationClusterSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = BaseStationCluster
        geo_field = 'point'
        fields = ('id', 'zoom_size', 'count', 'data')
