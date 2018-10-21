from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from base_station.models import (
    Operator, MNC, OwnedBaseStation, IdentifiedBaseStation)


admin.site.register(Operator, LeafletGeoAdmin)
admin.site.register(MNC, LeafletGeoAdmin)
admin.site.register(OwnedBaseStation, LeafletGeoAdmin)
admin.site.register(IdentifiedBaseStation, LeafletGeoAdmin)
