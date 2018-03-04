from django.contrib.gis import admin

from base_station.models import (
    OwnedBaseStation, IdentifiedBaseStation, Topography)


admin.site.register(OwnedBaseStation, admin.GeoModelAdmin)
admin.site.register(IdentifiedBaseStation, admin.GeoModelAdmin)
admin.site.register(Topography, admin.GeoModelAdmin)

