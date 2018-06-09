from django.contrib.gis.geos import Point
from functools import reduce
from math import log10

from optimization.utils import dbsum, geographic_distance,grouper
from optimization.models import OptimizedBaseStation


class AreaOptimization():

    def objective(self, current_bss_list, new_bss):
        covered_area_by_bs = list(map(lambda bs: bs.covered_area, current_bss_list))
        bs_objects = [OptimizedBaseStation(point = Point(bs[0], bs[1]))
                    for bs in grouper(new_bss, 2)]
        new_bss_covered_area = map(lambda bs: bs.covered_area, bs_objects)
        new_bss_union = reduce(lambda bs0, bs1: bs0 | bs1, new_bss_covered_area)
        bss_union = reduce(lambda x, y: x | y, covered_area_by_bs)
        total_area = (new_bss_union | bss_union).area
        return -(total_area)


class FreeSpacePathLossOptimization():

    def free_space_path_loss(self, distance, frequency):
        return 20 * log10(distance) + 20 * log10(frequency) - 32.45

    def objective(self, current_bss_list, new_bss):
        frequency = 1800
        total_path_loss = 0
        for bss in current_bss_list:
            distance = geographic_distance(bss.point.x, bss.point.y, new_bss[0], new_bss[1])
            path_loss = self.free_space_path_loss(distance, frequency)
            total_path_loss = dbsum(total_path_loss, path_loss)
        return total_path_loss
