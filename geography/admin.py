from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from geography.models import (
    Topography, FederativeUnit)


admin.site.register(Topography, LeafletGeoAdmin)
admin.site.register(FederativeUnit, LeafletGeoAdmin)
