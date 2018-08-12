from rest_framework.fields import SerializerMethodField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import BaseStationCluster


class BaseStationClusterSerializer(GeoFeatureModelSerializer):
    geohash = SerializerMethodField()

    class Meta:
        model = BaseStationCluster
        geo_field = 'point'
        fields = ('id', 'precision', 'geohash', 'count', 'data')

    @staticmethod
    def get_geohash(obj):
        return obj.geohash
