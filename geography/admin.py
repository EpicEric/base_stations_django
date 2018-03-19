from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from geography.models import FederativeUnit


admin.site.register(FederativeUnit, LeafletGeoAdmin)
