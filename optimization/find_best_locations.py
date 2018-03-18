from django.contrib.gis.geos import Point
from functools import reduce
import numpy as np
from scipy.optimize import minimize
import itertools
from optimization.models import OptimizedBaseStation

def grouper(iterable, group_size):
    return list(zip(*(iter(iterable),) * group_size))


def objective(covered_area_by_bs, new_bss):
    bs_objects = [OptimizedBaseStation(point = Point(bs[0], bs[1]))
                  for bs in grouper(new_bss, 2)]
    new_bss_covered_area = map(lambda bs: bs.covered_area, bs_objects)
    new_bss_union = reduce(lambda bs0, bs1: bs0 | bs1, new_bss_covered_area)
    bss_union = reduce(lambda x, y: x | y, covered_area_by_bs)
    total_area = (new_bss_union | bss_union).area
    return -(total_area)

def find_best_locations(base_stations, number, bounds):
    x = np.linspace(bounds[0][0], bounds[0][1], number)
    y = (bounds[1][1] - bounds[1][0])/2 + bounds[1][0]
    x0 = [Point(xi, y) for xi in x]

    covered_area_by_bs = list(map(lambda bs: bs.covered_area, base_stations))

    solution = minimize(lambda bss: objective(covered_area_by_bs, bss),
                        x0,
                        method='SLSQP',
                        bounds=bounds * number)
    return solution
