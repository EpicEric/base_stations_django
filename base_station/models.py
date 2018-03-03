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
    radio = models.CharField(max_length=10)
    mcc = models.IntegerField()
    mnc = models.IntegerField()
    lac = models.IntegerField()
    cid = models.IntegerField()
    point = models.PointField()
    averageSignal = models.FloatField()

    def __str__(self):
        return "{}-{}-{}-{}".format(self.mcc, self.mnc, self.lac, self.cid)
