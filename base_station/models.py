from django.contrib.gis.db import models

class BaseStation(models.Model):
    operator = models.CharField(max_length=40)
    state = models.CharField(max_length=2)
    municipality = models.CharField(max_length=40)
    address = models.CharField(max_length=200, null=True, blank=True)
    point = models.PointField()

    def __str__(self):
        return "{} ({}) - {}".format(self.municipality, self.state, self.address)

class BaseStationWithLocation(models.Model):
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
    averageSignal = models.FloatField()

    def __str__(self):
        return "{}-{}-{}-{}".format(self.mcc, self.mnc, self.lac, self.cid)

class Topography(models.Model):
    point = models.PointField()

    def __str__(self):
        return "LONG:{}, LAT:{}, ALT:{}".format(self.point[0], self.point[1], self.point[2])
