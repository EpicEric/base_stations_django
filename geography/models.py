from django.contrib.gis.db import models


class FederativeUnit(models.Model):
    name = models.CharField(max_length=40, blank=True)
    short = models.CharField(max_length=2)
    country = models.CharField(max_length=40, default='Brazil')

    def __str__(self):
        return '{} ({})'.format(self.name or self.short, self.country)
