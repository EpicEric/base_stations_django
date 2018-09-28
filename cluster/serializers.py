from rest_framework.fields import SerializerMethodField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import BaseStationCluster, BS_MODEL


class BaseStationClusterSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = BaseStationCluster
        geo_field = 'point'
        fields = ('id', 'count', 'data')


class BaseStationUnitSerializer(GeoFeatureModelSerializer):
    count = SerializerMethodField()
    data = SerializerMethodField()

    class Meta:
        model = BS_MODEL
        geo_field = 'point'
        fields = ('id', 'count', 'data')

    @staticmethod
    def get_count(_):
        return 1

    @staticmethod
    def get_data(obj):
        return obj.data
