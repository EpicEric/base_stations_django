from django.contrib.gis.geos import Point
from functools import reduce
from math import log10

from optimization.utils import dbsum, geographic_distance,grouper
from optimization.models import OptimizedBaseStation
from optimization.utils import timing


class AreaOptimization():
    def __init__(self):
        self.test = 0
        self.covered_area_by_bs = 0
        self.bss_union = 0

    @timing
    def objective(self, current_bss_list, new_bss):
        if self.covered_area_by_bs == 0:
            self.covered_area_by_bs = list(map(lambda bs: bs.covered_area, current_bss_list))
            self.bss_union = reduce(lambda x, y: x | y, self.covered_area_by_bs)
        
        bs_objects = [OptimizedBaseStation(point = Point(bs[0], bs[1]))
                    for bs in grouper(new_bss, 2)]
        new_bss_covered_area = map(lambda bs: bs.covered_area, bs_objects)
        new_bss_union = reduce(lambda bs0, bs1: bs0 | bs1, new_bss_covered_area)
        total_area = (new_bss_union | self.bss_union).area
        self.test += 1
        print("Teste é: "+str(self.test))
        return -(total_area)


class FreeSpacePathLossOptimization():

    def free_space_path_loss(self, distance, frequency):
        return 20 * log10(distance) + 20 * log10(frequency) - 32.45

    def objective(self, current_bss_list, new_bss):
        frequency = 1800
        total_path_loss = 0
        min_distance = None
        for bss in current_bss_list:
            distance = geographic_distance(bss.point.x, bss.point.y, new_bss[0], new_bss[1])
            if not min_distance or distance < min_distance:
                min_distance = distance
                path_loss = self.free_space_path_loss(min_distance, frequency)
        return total_path_loss
