from base_station.models import IdentifiedBaseStation
from django.db import connection
from django.contrib.gis.geos import GEOSGeometry, Polygon
from django.core.cache import caches
import math

cache = caches['db_cache']
BS_MODEL = IdentifiedBaseStation
DB_TABLE = BS_MODEL._meta.db_table
MAX_CACHE_ZOOM = 16
CLUSTER_EPS_BASE = 70.0


def tile_to_bbox(x_tile, y_tile, zoom_size):
    n = 2.0 ** zoom_size
    left_deg = x_tile / n * 360.0 - 180.0
    right_deg = (x_tile + 1) / n * 360.0 - 180.0
    top_deg = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y_tile / n))))
    bottom_deg = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (y_tile + 1) / n))))
    return tuple((left_deg, bottom_deg, right_deg, top_deg))


class Cluster(object):
    def __init__(self, point, zoom_size, base_stations):
        self.point = GEOSGeometry(point)
        self.zoom_size = zoom_size
        self.count = len(base_stations)
        if self.count == 1:
            self.cgi = base_stations.get().cgi
        else:
            self.cgi = ""

    def __str__(self):
        if self.count == 1:
            return "{} ({})".format(self.point, self.cgi)
        return "{} ({} stations)".format(self.point, self.count)

    @property
    def base_stations(self):
        return BS_MODEL.objects.filter(point__distance_lte=(self.point, Cluster.cluster_eps(self.zoom_size)))

    @staticmethod
    def get_clusters(x_tile, y_tile, zoom_size):
        if zoom_size <= MAX_CACHE_ZOOM:
            cluster_list = cache.get_or_set(
                'cluster/{}/{}/{}'.format(zoom_size, x_tile, y_tile),
                lambda: Cluster.get_clusters_for_tile(x_tile, y_tile, zoom_size),
                None)
        else:
            cluster_list = Cluster.get_clusters_for_tile(x_tile, y_tile, zoom_size)
        return cluster_list

    @staticmethod
    def get_clusters_for_tile(x_tile, y_tile, zoom_size):
        bbox = tile_to_bbox(x_tile, y_tile, zoom_size)
        cluster_eps = Cluster.cluster_eps(zoom_size)
        bbox_poly = Polygon.from_bbox(bbox)
        base_stations = BS_MODEL.objects.filter(point__contained=bbox_poly)

        kmeans_query = """
        SELECT
            unnest(ST_ClusterWithin(point, %s))
        FROM
            {}
        WHERE
            id = ANY(%s);""".format(DB_TABLE)
        with connection.cursor() as cursor:
            cursor.execute(kmeans_query, [cluster_eps, [bs.id for bs in base_stations]])
            cluster_rows = cursor.fetchall()

        cluster_collections = [GEOSGeometry(row[0]) for row in cluster_rows]
        clusters = list(map(
            lambda coll: Cluster(coll.centroid, zoom_size, base_stations.filter(point__contained=coll)),
            cluster_collections))
        return clusters

    @staticmethod
    def cluster_eps(zoom_size):
        n = 2.0 ** zoom_size
        return CLUSTER_EPS_BASE / n
