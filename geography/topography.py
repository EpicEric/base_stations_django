from django.contrib.gis.geos import Point, GEOSGeometry
import ee
import json
import numpy as np


ee.Initialize()
world_dem_image = ee.Image('USGS/SRTMGL1_003')


class TopographyData(object):
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
        self.polygon_map = None

    def get_topography_data(self):
        topography_data_list = []
        if not self.polygon_map:
            self.polygon_map = {}
            for feature in self.collection['features']:
                population_count = feature['properties']['label']
                polygon = GEOSGeometry(json.dumps(feature['geometry']))
                if self.polygon_map.get(population_count):
                    self.polygon_map[population_count] = self.polygon_map[population_count].union(polygon)
                else:
                    self.polygon_map[population_count] = polygon
        minimum_longitude = (np.around(self.bbox[0] * 3600) + 1) / 3600
        maximum_longitude = self.bbox[2]
        minimum_latitude = (np.around(self.bbox[1] * 3600) + 1) / 3600
        maximum_latitude = self.bbox[3]
        for longitude in np.arange(minimum_longitude, maximum_longitude, 1/3600):
            for latitude in np.arange(minimum_latitude, maximum_latitude, 1/3600):
                point = Point(longitude, latitude)
                for k, v in self.polygon_map.items():
                    if v.contains(point):
                        topography_data_list.append(TopographyData(point, k))
                        break
        return topography_data_list
