from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon
from geography.models import FederativeUnit


class Operator(models.Model):
    name = models.CharField(max_length=40)
    friendly_name = models.CharField(max_length=40, blank=True)
    number = models.CharField(max_length=20, blank=True)
    cnpj = models.CharField(max_length=20, blank=True)
    fistel = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.friendly_name if self.friendly_name else self.name

class MNC(models.Model):
    value = models.IntegerField()
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.value, self.operator)


class BaseStation(models.Model):
    point = models.PointField()

    class Meta:
        abstract = True

    @property
    def covered_area(self):
        # FIXME
        return self.point.buffer(1/220)

    @classmethod
    def get_base_stations_inside_bounds(cls, min_lon, min_lat, max_lon, max_lat):
        bounds = (min_lon, min_lat, max_lon, max_lat)
        geom = Polygon.from_bbox(bounds)
        return cls.objects.filter(point__contained=geom)


class OwnedBaseStation(BaseStation):
    operator = models.ForeignKey(Operator, null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(FederativeUnit, null=True, on_delete=models.SET_NULL)
    municipality = models.CharField(max_length=40)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return "{} ({}) - {}".format(self.municipality, self.state.short, self.address)


class IdentifiedBaseStation(BaseStation):
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
    average_signal = models.FloatField(null=True)

    @property
    def cgi(self):
        return "{}-{}-{}-{}".format(self.mcc, self.mnc, self.lac, self.cid)

    @property
    def data(self):
        return "{} ({})".format(self.cgi, self.radio)

    def __str__(self):
        return self.data
