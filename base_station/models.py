from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon
from geography.models import FederativeUnit

class Operator(models.Model):
    name = models.CharField(max_length=40)
    number = models.CharField(max_length=20, blank=True)
    cnpj = models.CharField(max_length=20, blank=True)
    fistel = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class OwnedBaseStation(models.Model):
    operator = models.ForeignKey(Operator, null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(FederativeUnit, null=True, on_delete=models.SET_NULL)
    municipality = models.CharField(max_length=40)
    address = models.CharField(max_length=200, null=True, blank=True)
    point = models.PointField()

    def __str__(self):
        return "{} ({}) - {}".format(self.municipality, self.state.short, self.address)


class IdentifiedBaseStation(models.Model):
    RADIOS = (
        ('GSM', 'Global System for Mobile Communications'),
        ('UMTS', 'Universal Mobile Telecommunications System'),
        ('LTE', 'Long-Term Evolution'),
        ('CDMA', 'Code-division multiple access'),
    )

    radio = models.CharField(max_length=4, choices=RADIOS)
    mcc = models.PositiveIntegerField()
    mnc = models.PositiveIntegerField()
    lac = models.PositiveIntegerField()
    cid = models.PositiveIntegerField()
    point = models.PointField()
    average_signal = models.FloatField(null=True)

    @property
    def cgi(self):
        return "{}-{}-{}-{}".format(self.mcc, self.mnc, self.lac, self.cid)

    @property
    def covered_area(erb):
        #FIXME
        return erb.point.buffer(1)

    @staticmethod
    def get_base_stations_inside_bounds(min_lon, min_lat, max_lon, max_lat):
        bounds = (min_lon, min_lat, max_lon, max_lat)
        geom = Polygon.from_bbox(bounds)
        return IdentifiedBaseStation.objects.filter(point__contained=geom)

    def __str__(self):
        return "{} ({})".format(self.cgi, self.radio)
