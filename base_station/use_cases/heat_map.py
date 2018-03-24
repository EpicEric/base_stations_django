import numpy as np
import itertools

from base_station.models import IdentifiedBaseStation
from optimization.find_best_locations import OptimizeLocation



class HeatMap():
    def __init__(self, bss, bounds):
        self.bss = bss
        self.bounds = bounds

    def __scale_heatmap(self, heatmap):
        MAX_HEATMAP = 3500
        MIN_HEATMAP = 1

        min_value = heatmap[0][2]
        max_value = heatmap[-1][2]

        return list(map(lambda p: [
            p[0],
            p[1],
            (p[2] - min_value)*(MAX_HEATMAP - MIN_HEATMAP)/
                (max_value - min_value) + MIN_HEATMAP], heatmap))

    def generate_heatmap(self):
        covered_area_by_bs = list(map(lambda bs: bs.covered_area, self.bss))

        x = np.linspace(self.bounds[0][0], self.bounds[0][1], num=100)
        y = np.linspace(self.bounds[1][0], self.bounds[1][1], num=100)
        coord = [list(e) for e in itertools.product(x,y)]
        heatmap = map(lambda coord: [
            coord[1], coord[0], (-OptimizeLocation.objective(covered_area_by_bs, coord))*110*110,
            ], coord)

        heatmap = sorted(heatmap, key=lambda x: x[2])
        return self.__scale_heatmap(heatmap)
