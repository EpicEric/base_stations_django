from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from cluster.models import BaseStationCluster


admin.site.register(BaseStationCluster, LeafletGeoAdmin)
