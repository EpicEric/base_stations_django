from django.contrib.gis.geos import Point, GEOSGeometry
import ee
import json
import numpy as np


ee.Initialize()
brazil_pop_collection = ee.ImageCollection('WorldPop/POP').filter(ee.Filter.eq('system:index', 'BRA_2015'))
brazil_pop_image = ee.Image(brazil_pop_collection.toList(1).get(0)).round().toInt()


class PopulationData(object):
    def __init__(self, point, count):
        self.point = point
        self.count = count


class PopulationBBox(object):
    def __init__(self, bbox):
        self.bbox = bbox
        area = ee.Geometry.Polygon(bbox[0], bbox[1], bbox[0], bbox[3], bbox[2], bbox[3],
                                   bbox[2], bbox[1], bbox[0], bbox[1])
        vectors = brazil_pop_image.reduceToVectors(geometry=area)
        self.collection = vectors.getInfo()
        self.polygon_map = None

    def get_population_data(self):
        population_data_list = []
        if not self.polygon_map:
            self.polygon_map = {}
            for feature in self.collection['features']:
                population_count = feature['properties']['label']
                polygon = GEOSGeometry(json.dumps(feature['geometry']))
                if self.polygon_map.get(population_count):
                    self.polygon_map[population_count] = self.polygon_map[population_count].union(polygon)
                else:
                    self.polygon_map[population_count] = polygon
        for longitude in np.arange(np.around(self.bbox[0], decimals=3), self.bbox[2], 0.001):
            for latitude in np.arange(np.around(self.bbox[1], decimals=3), self.bbox[3], 0.001):
                point = Point(longitude, latitude)
                for k, v in self.polygon_map.items():
                    if v.contains(point):
                        if k > 0:
                            population_data_list.append(PopulationData(point, k))
                        break
        return population_data_list
