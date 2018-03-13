from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import IdentifiedBaseStation


class IdentifiedBaseStationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = IdentifiedBaseStation
        geo_field = 'point'
        fields = ('id', 'cgi', 'radio', 'average_signal')