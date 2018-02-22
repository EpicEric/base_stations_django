from django.contrib.gis import admin

from base_station.models import BaseStation


#admin.site.register(BaseStation, admin.OSMGeoAdmin)
admin.site.register(BaseStation, admin.GeoModelAdmin)

