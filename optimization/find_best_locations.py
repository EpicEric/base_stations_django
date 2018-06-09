from django.contrib.gis.geos import Point
import numpy as np
from optimization.models import OptimizedBaseStation
from optimization.utils import grouper

class OptimizeLocation():

    def __init__(self, current_bss_list, bounds,
                 optimization_method, objective):
        self.current_bss_list = current_bss_list
        self.bounds = bounds
        self.objective = objective
        self.optimization_method = optimization_method

    def find_best_locations(self):
        x = np.linspace(self.bounds[0][0], self.bounds[0][1], len(self.bounds)/2)
        y = (self.bounds[1][1] - self.bounds[1][0])/2 + self.bounds[1][0]
        x0 = [Point(xi, y) for xi in x]

        solution = self.optimization_method.minimize(
            lambda new_bss_location: self.objective(self.current_bss_list, 
                                                    new_bss_location),
            self.bounds,
            x0)
        return grouper(solution.x, 2)
