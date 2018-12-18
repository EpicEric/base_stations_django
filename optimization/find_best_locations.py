from django.contrib.gis.geos import Point
from functools import reduce
import numpy as np
from scipy.optimize import minimize, basinhopping
from optimization.models import OptimizedBaseStation
from optimization.taguchi import taguchi
import random

class OptimizeLocation():

    @staticmethod
    def grouper(iterable, group_size):
        return list(zip(*(iter(iterable),) * group_size))

    @staticmethod
    def objective(covered_area_by_bs, new_bss):
        bs_objects = [OptimizedBaseStation(point = Point(bs[1], bs[0]))
                    for bs in OptimizeLocation.grouper(new_bss, 2)]
        new_bss_covered_area = map(lambda bs: bs.covered_area, bs_objects)
        new_bss_union = reduce(lambda bs0, bs1: bs0 | bs1, new_bss_covered_area)
        bss_union = reduce(lambda x, y: x | y, covered_area_by_bs)
        total_area = (new_bss_union | bss_union).area
        return -(total_area)

    def basinhopping(base_stations, number, bounds):
        x = np.linspace(bounds[1][0], bounds[1][1], number)
        y = (bounds[0][1] - bounds[0][0])/2 + bounds[0][0]
        x0 = [Point(xi, y) for xi in x]

        minimizer_kwargs = {"method":"L-BFGS-B", "bounds": bounds * number}
        covered_area_by_bs = list(map(lambda bs: bs.covered_area, base_stations))
        solution = basinhopping(lambda x: OptimizeLocation.objective(covered_area_by_bs, x), x0, minimizer_kwargs=minimizer_kwargs,
                    niter=10)
        print(solution.x)
        return OptimizeLocation.grouper(solution.x, 2)

    def slsqp(base_stations, number, bounds):
        x = np.linspace(bounds[0][0], bounds[0][1], number)
        y = (bounds[1][1] - bounds[1][0])/2 + bounds[1][0]
        x0 = [Point(xi, y) for xi in x]

        covered_area_by_bs = list(map(lambda bs: bs.covered_area, base_stations))

        solution = minimize(lambda bss: OptimizeLocation.objective(covered_area_by_bs, bss),
                            x0,
                            method='SLSQP',
                            bounds=bounds * number,
                            options={'eps': 0.1})
        return OptimizeLocation.grouper(solution.x, 2)

    def taguchi(base_stations, number, bounds):
        x = np.linspace(bounds[0][0], bounds[0][1], number)
        y = (bounds[1][1] - bounds[1][0])/2 + bounds[1][0]
        x0 = [Point(xi, y) for xi in x]

        covered_area_by_bs = list(map(lambda bs: bs.covered_area, base_stations))
        solution = taguchi(bounds * number, 3, lambda bss: OptimizeLocation.objective(covered_area_by_bs, bss), 0.9)
        print(solution)
        return OptimizeLocation.grouper(solution['x'], 2)

    def random_search(base_stations, number, bounds, iterations):
        covered_area_by_bs = list(map(lambda bs: bs.covered_area, base_stations))
        solution = {"x": 0, "y": 0, "area": 0}

        for i in range(iterations):
            random_x = random.uniform(bounds[0][0], bounds[0][1])
            random_y = random.uniform(bounds[1][0], bounds[1][1])
            area = -1*(OptimizeLocation.objective(covered_area_by_bs, [random_x, random_y]))
            if area > solution["area"]:
                solution["area"] = area
                solution["x"] = random_x
                solution["y"] = random_y
        return [(solution["x"], solution["y"])]