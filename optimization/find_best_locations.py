from django.contrib.gis.geos import Point
from functools import reduce
import numpy as np
from scipy.optimize import minimize

from optimization.models import OptimizedBaseStation


def objective(covered_area_by_bs, new_bs):
    new_bs = OptimizedBaseStation(point = Point(new_bs[0], new_bs[1]))
    new_bs_covered_area = new_bs.covered_area
    total_area = (reduce(lambda x, y: x | y, covered_area_by_bs) | 
                  new_bs_covered_area).area
    return -(total_area)


def find_best_locations(base_stations, bounds):
    covered_area_by_bs = list(map(lambda bs: bs.covered_area, base_stations))
    x0 = Point((bounds[0][1] - bounds[0][0])/2 + bounds[0][0],
               (bounds[1][1] - bounds[1][0])/2 + bounds[1][0])
    solution = minimize(lambda bs: objective(covered_area_by_bs, bs),
                        x0,
                        method='SLSQP',
                        bounds=bounds)
    return solution
