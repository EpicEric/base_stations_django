from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Point
import ee
import json
import numpy as np

from geography.models import Population


ee.Initialize()
brazil_pop_collection = ee.ImageCollection('WorldPop/POP').filter(ee.Filter.eq('system:index', 'BRA_2015'))
brazil_pop_image = ee.Image(brazil_pop_collection.toList(1).get(0)).round().toInt()


class PopulationPoint(object):
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
                population = Population(poly=v, count=k)
                population.save()
            self.saved = True

    def get_population_points(self):
        if not self.saved:
            self.save()
        population_point_list = []
        minimum_longitude = np.around(self.bbox[0] + 0.001, decimals=3)
        maximum_longitude = self.bbox[2]
        minimum_latitude = np.around(self.bbox[1] + 0.001, decimals=3)
        maximum_latitude = self.bbox[3]
        for longitude in np.arange(minimum_longitude, maximum_longitude, 0.001):
            for latitude in np.arange(minimum_latitude, maximum_latitude, 0.001):
                point = Point(longitude, latitude)
                query = Population.objects.filter(poly__contains=point)
                if query.exists():
                    population_point_list.append(PopulationPoint(point, query.first().count))
        return population_point_list
