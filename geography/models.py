from django.contrib.gis.db import models


class Topography(models.Model):
    point = models.PointField()
    altitude = models.PositiveIntegerField()

    def __str__(self):
        return "LONG:{}, LAT:{}, ALT:{}".format(
            self.point[0], self.point[1], self.altitude)


class FederativeUnit(models.Model):
    name = models.CharField(max_length=40, blank=True)
    short = models.CharField(max_length=2)
    country = models.CharField(max_length=40, default='Brazil')

    def __str__(self):
        return '{} ({})'.format(self.name or self.short, self.country)
