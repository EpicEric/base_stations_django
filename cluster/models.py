from django.contrib.gis.db import models
from django.db import connection
from django.contrib.gis.geos import GEOSGeometry, Point
from functools import reduce
import math

from base_station.models import IdentifiedBaseStation

BS_MODEL = IdentifiedBaseStation
DB_TABLE = BS_MODEL._meta.db_table
MAX_CACHE_ZOOM_SIZE = 16
CLUSTER_EPS_MAX = 120.0
CLUSTER_EPS_MIN = 70.0


def tile_to_bbox(x_tile, y_tile, zoom_size):
    n = 2.0 ** zoom_size
    left_deg = x_tile / n * 360.0 - 180.0
    right_deg = (x_tile + 1) / n * 360.0 - 180.0
    top_deg = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y_tile / n))))
    bottom_deg = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (y_tile + 1) / n))))
    return tuple((left_deg, bottom_deg, right_deg, top_deg))


class BaseStationCluster(models.Model):
    point = models.PointField()
    zoom_size = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    data = models.CharField(max_length=40, blank=True)

    def __str__(self):
        if self.count == 1:
            return "{} ({})".format(self.point, self.data)
        return "{} ({} stations)".format(self.point, self.count)

    @property
    def base_stations(self):
        return BS_MODEL.objects.filter(point__distance_lte=(self.point, BaseStationCluster.cluster_eps(self.zoom_size)))

    @classmethod
    def generate_clusters(cls, zoom_size):
        if not cls.objects.filter(zoom_size=zoom_size).exists():
            if 0 <= zoom_size < MAX_CACHE_ZOOM_SIZE:
                print("Generating clusters...")
                cluster_eps = cls.cluster_eps(zoom_size)
                kmeans_query = """
                SELECT
                    unnest(ST_ClusterWithin(point, %s))
                FROM
                    {} WHERE zoom_size = %s;""".format(cls._meta.db_table)
                with connection.cursor() as cursor:
                    cursor.execute(kmeans_query, [cluster_eps, zoom_size + 1])
                    cluster_rows = cursor.fetchall()

                cluster_collections = [GEOSGeometry(row[0]) for row in cluster_rows]
                total = len(cluster_collections)
                if not total:
                    raise ValueError("No clusters found for zoom size {}".format(zoom_size + 1))
                print("Saving data for {} clusters...".format(total))
                counter = 0
                percentage = 0
                for coll in cluster_collections:
                    clusters = cls.objects.filter(zoom_size=zoom_size + 1, point__contained=coll)
                    count = reduce((lambda acc, cl: acc + cl.count), clusters, 0)
                    data = clusters.first().data if count == 1 else ''
                    point = Point(
                        reduce((lambda acc, cl: acc + (cl.point.x * float(cl.count))), clusters, 0.0)
                        / float(count),
                        reduce((lambda acc, cl: acc + (cl.point.y * float(cl.count))), clusters, 0.0)
                        / float(count)
                    )
                    cluster = BaseStationCluster(
                        point=point,
                        zoom_size=zoom_size,
                        count=count,
                        data=data)
                    cluster.save()
                    counter += 1
                    prev_percentage = percentage
                    percentage = int(100 * counter // total)
                    if percentage > prev_percentage:
                        print(" {}% done ({} clusters)".format(percentage, counter))

            elif zoom_size == MAX_CACHE_ZOOM_SIZE:
                print("Generating clusters...")
                cluster_eps = cls.cluster_eps(zoom_size)
                kmeans_query = """
                SELECT
                    unnest(ST_ClusterWithin(point, %s))
                FROM
                    {};""".format(DB_TABLE)
                with connection.cursor() as cursor:
                    cursor.execute(kmeans_query, [cluster_eps])
                    cluster_rows = cursor.fetchall()

                cluster_collections = [GEOSGeometry(row[0]) for row in cluster_rows]
                total = len(cluster_collections)
                print("Saving data for {} clusters...".format(total))
                counter = 0
                percentage = 0
                for coll in cluster_collections:
                    base_stations = BS_MODEL.objects.filter(point__contained=coll)
                    count = base_stations.count()
                    bs = base_stations.first() if count == 1 else None
                    data = '{} ({})'.format(bs.cgi, bs.radio) if bs else ''
                    point = coll.centroid
                    cluster = BaseStationCluster(
                        point=point,
                        zoom_size=zoom_size,
                        count=count,
                        data=data)
                    cluster.save()
                    counter += 1
                    prev_percentage = percentage
                    percentage = int(100 * counter // total)
                    if percentage > prev_percentage:
                        print(" {}% done ({} clusters)".format(percentage, counter))

            else:
                raise ValueError("zoom_size must be in the [0, {}] interval".format(MAX_CACHE_ZOOM_SIZE))

        else:
            raise ValueError("There are already clusters for zoom size {}".format(zoom_size))

    @staticmethod
    def cluster_eps(zoom_size):
        n = 2.0 ** zoom_size
        return (CLUSTER_EPS_MAX * zoom_size + CLUSTER_EPS_MIN * (MAX_CACHE_ZOOM_SIZE - zoom_size)) \
               / (MAX_CACHE_ZOOM_SIZE * n)
