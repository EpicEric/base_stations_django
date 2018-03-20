from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Point
import ee
import json
import numpy as np

from geography.models import Topography


ee.Initialize()
world_dem_image = ee.Image('USGS/SRTMGL1_003')


class TopographyPoint(object):
    def __init__(self, point, altitude):
        self.point = point
        self.altitude = altitude


class TopographyBBox(object):
    def __init__(self, bbox):
        self.bbox = bbox
        area = ee.Geometry.Polygon(bbox[0], bbox[1], bbox[0], bbox[3], bbox[2], bbox[3],
                                   bbox[2], bbox[1], bbox[0], bbox[1])
        vectors = world_dem_image.reduceToVectors(geometry=area)
        self.collection = vectors.getInfo()
        self.saved = False

    def save(self):
        if not self.saved:
            polygon_map = {}
            for feature in self.collection['features']:
                population_count = feature['properties']['label']
                polygon = GEOSGeometry(json.dumps(feature['geometry']))
                if polygon_map.get(population_count):
                    polygon_map[population_count] = polygon_map[population_count].union(polygon)
                else:
                    polygon_map[population_count] = MultiPolygon(polygon)
            for k, v in polygon_map.items():
                topography = Topography(poly=v, altitude=k)
                topography.save()
            self.saved = True

    def get_topography_points(self):
        if not self.saved:
            self.save()
        topography_point_list = []
        minimum_longitude = (np.around(self.bbox[0] * 3600) + 1) / 3600
        maximum_longitude = self.bbox[2]
        minimum_latitude = (np.around(self.bbox[1] * 3600) + 1) / 3600
        maximum_latitude = self.bbox[3]
        for longitude in np.arange(minimum_longitude, maximum_longitude, 1/3600):
            for latitude in np.arange(minimum_latitude, maximum_latitude, 1/3600):
                point = Point(longitude, latitude)
                query = Topography.objects.filter(poly__contains=point)
                if query.exists():
                    topography_point_list.append(TopographyPoint(point, query.first().altitude))
        return topography_point_list
