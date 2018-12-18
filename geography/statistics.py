from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Point
import ee
from functools import reduce
import json
import numpy as np


ee.Initialize()
brazil_pop_collection = ee.ImageCollection('WorldPop/POP').filter(ee.Filter.eq('system:index', 'BRA_2015'))
brazil_pop_image = ee.Image(brazil_pop_collection.toList(1).get(0)).round().toInt()


def build_bbox(bs_list):
    bbox = (bs_list[0].point.x, bs_list[0].point.y, bs_list[0].point.x, bs_list.point.y)
    for bs in bs_list:
        x = bs.point.x
        y = bs.point.y
        if x < bbox[0]:
            bbox[0] = x
        elif x > bbox[2]:
            bbox[2] = x
        if y < bbox[1]:
            bbox[1] = y
        elif y > bbox[3]:
            bbox[3] = y
    return (bbox[0] - 1/220, bbox[1] - 1/220, bbox[2] + 1/220, bbox[3] + 1/220)


class PopulationStatistics(object):
    def __init__(self, optimized_bs_list):
        self.bs_list = optimized_bs_list
        self.bbox = build_bbox(self.bs_list)
        bs_area = reduce(lambda bs1, bs2: bs1 | bs2,
                         map(lambda bs: bs.covered_area, self.bs_list))
        current_bs = IdentifiedBaseStation.objects.filter(point__contained=Polygon.from_bbox(self.bbox))
        self.area = reduce(lambda acc, bs: acc - bs,
                           map(lambda bs: bs.covered_area, current_bs),
                           bs_area)
        area = ee.Geometry.Polygon(bbox[0], bbox[1], bbox[0], bbox[3], bbox[2], bbox[3],
                                   bbox[2], bbox[1], bbox[0], bbox[1])
        vectors = brazil_pop_image.reduceToVectors(geometry=area)
        self.collection = vectors.getInfo()
        self.built = False

    def build(self):
        if not self.built:
            self.polygon_map = {}
            for feature in self.collection['features']:
                population_count = feature['properties']['label']
                polygon = GEOSGeometry(json.dumps(feature['geometry']))
                if self.polygon_map.get(population_count):
                    self.polygon_map[population_count] = self.polygon_map[population_count].union(polygon)
                else:
                    self.polygon_map[population_count] = MultiPolygon(polygon)
            self.built = True

    def get_population_count(self):
        if not self.built:
            self.build()
        population_count = 0
        minimum_longitude = np.around(self.bbox[0] + 0.001, decimals=3)
        maximum_longitude = self.bbox[2]
        minimum_latitude = np.around(self.bbox[1] + 0.001, decimals=3)
        maximum_latitude = self.bbox[3]
        for longitude in np.arange(minimum_longitude, maximum_longitude, 0.001):
            for latitude in np.arange(minimum_latitude, maximum_latitude, 0.001):
                point = Point(longitude, latitude)
                if self.area.contains(point):
                    for k, v in self.polygon_map.items():
                        if v.contains(point):
                            population_count += k
                            break
        return population_count
