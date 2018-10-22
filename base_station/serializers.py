from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import IdentifiedBaseStation, Operator


class IdentifiedBaseStationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = IdentifiedBaseStation
        geo_field = 'point'
        fields = ('id', 'cgi', 'radio', 'average_signal')


class OperatorSerializer(ModelSerializer):
    class Meta:
        model = Operator
        fields = ('id', 'friendly_name', 'name', 'cnpj')
