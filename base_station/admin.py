from django.contrib.gis import admin

from base_station.models import (
    Operator, OwnedBaseStation, IdentifiedBaseStation)


admin.site.register(Operator, admin.GeoModelAdmin)
admin.site.register(OwnedBaseStation, admin.GeoModelAdmin)
admin.site.register(IdentifiedBaseStation, admin.GeoModelAdmin)
