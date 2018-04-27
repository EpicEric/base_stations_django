from base_station.models import IdentifiedBaseStation
from django.db import connection
from django.contrib.gis.geos import GEOSGeometry
from django.core.cache import cache
import math

DB_TABLE = IdentifiedBaseStation._meta.db_table
MAX_CACHE_ZOOM = 16
CLUSTER_EPS_BASE = 110.0


def tile_to_bbox(x_tile, y_tile, zoom_size):
    n = 2.0 ** zoom_size
    left_deg = x_tile / n * 360.0 - 180.0
    right_deg = (x_tile + 1) / n * 360.0 - 180.0
    top_deg = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y_tile / n))))
    bottom_deg = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (y_tile + 1) / n))))
    return tuple((left_deg, bottom_deg, right_deg, top_deg))


class Cluster(object):
    def __init__(self, point, zoom_size, count, mcc, mnc, lac, cid):
        self.point = GEOSGeometry(point)
        self.zoom_size = zoom_size
        self.count = count
        if self.count == 1:
            self.cgi = "{}-{}-{}-{}".format(mcc, mnc, lac, cid)
        else:
            self.cgi = ""

    def __str__(self):
        if self.count == 1:
            return "{} ({})".format(self.point, self.cgi)
        return "{} ({} stations)".format(self.point, self.count)

    # TODO: Verify if this works properly
    def get_base_stations(self):
        return IdentifiedBaseStation.objects.filter(point__distance_lte=(self.point, self.cluster_eps(self.zoom_size)))

    @staticmethod
    def get_clusters(x_tile, y_tile, zoom_size):
        if zoom_size <= MAX_CACHE_ZOOM:
            cluster_list = cache.get_or_set(
                'cluster/{}/{}/{}'.format(zoom_size, x_tile, y_tile),
                lambda: Cluster.cache_clusters_from_tile(x_tile, y_tile, zoom_size),
                None)
        else:
            cluster_list = Cluster.cache_clusters_from_tile(x_tile, y_tile, zoom_size)
        return cluster_list

    @staticmethod
    def cache_clusters_from_tile(x_tile, y_tile, zoom_size):
        bbox = tile_to_bbox(x_tile, y_tile, zoom_size)
        cluster_eps = Cluster.cluster_eps(zoom_size)

        kmeans_query = """
        SELECT
            MIN(id) as id,
            ST_Centroid(ST_Collect(point)) as point,
            COUNT(*) as count,
            MIN(mcc) as mcc,
            MIN(mnc) as mnc,
            MIN(lac) as lac,
            MIN(cid) as cid
        FROM (
            SELECT id, point, mcc, mnc, lac, cid, ST_ClusterDBSCAN(point, eps := %s, minpoints := 1) OVER()
                as cluster_id
            FROM {}
            WHERE point && ST_MakeEnvelope(%s, %s, %s, %s, 4326)
        ) AS kmeans
        GROUP BY cluster_id;""".format(DB_TABLE)
        with connection.cursor() as cursor:
            cursor.execute(kmeans_query, [cluster_eps, bbox[0], bbox[1], bbox[2], bbox[3]])
            clusters_rows = cursor.fetchall()

        clusters = list(map(
            lambda row: Cluster(row[1], zoom_size, row[2], row[3], row[4], row[5], row[6]),
            clusters_rows))
        return clusters

    @staticmethod
    def cluster_eps(zoom_size):
        n = 2.0 ** zoom_size
        return CLUSTER_EPS_BASE / n
