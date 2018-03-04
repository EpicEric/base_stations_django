from django.contrib.gis import admin

from geography.models import (
    Topography, FederativeUnit)


admin.site.register(Topography, admin.GeoModelAdmin)
admin.site.register(FederativeUnit, admin.GeoModelAdmin)
