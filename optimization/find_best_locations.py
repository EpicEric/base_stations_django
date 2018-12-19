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
        if len(covered_area_by_bs) > 0:
            bss_union = reduce(lambda x, y: x | y, covered_area_by_bs)
            total_area = (new_bss_union | bss_union).area
        else:
            total_area = new_bss_union.area
        return -(total_area)

    def basinhopping(base_stations, number, bounds):
        x = np.linspace(bounds[1][0], bounds[1][1], number)
        y = (bounds[0][1] - bounds[0][0])/2 + bounds[0][0]
        x0 = [Point(xi, y) for xi in x]

        minimizer_kwargs = {"method":"L-BFGS-B", "bounds": bounds * number}
        covered_area_by_bs = list(map(lambda bs: bs.covered_area, base_stations))
        solution = basinhopping(lambda x: OptimizeLocation.objective(covered_area_by_bs, x), x0, minimizer_kwargs=minimizer_kwargs,
                    niter=10)
        area = -OptimizeLocation.objective(covered_area_by_bs, solution.x)
        return (OptimizeLocation.grouper(solution.x, 2), area)

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
        area = -OptimizeLocation.objective(covered_area_by_bs, solution.x)
        return (OptimizeLocation.grouper(solution.x, 2), area)

    def taguchi(base_stations, number, bounds):
        x = np.linspace(bounds[0][0], bounds[0][1], number)
        y = (bounds[1][1] - bounds[1][0])/2 + bounds[1][0]
        x0 = [Point(xi, y) for xi in x]

        covered_area_by_bs = list(map(lambda bs: bs.covered_area, base_stations))
        solution = taguchi(bounds * number, 3, lambda bss: OptimizeLocation.objective(covered_area_by_bs, bss), 0.9)
        area = -OptimizeLocation.objective(covered_area_by_bs, solution['x'])
        return (OptimizeLocation.grouper(solution['x'], 2), area)

    def random_search(base_stations, number, bounds, iterations):
        covered_area_by_bs = list(map(lambda bs: bs.covered_area, base_stations))
        solution = {"new_bss": [], "area": 0}
        
        for i in range(iterations):
            random_x = []
            random_y = []
            new_bss = []
            for j in range(number):
                random_x.append(random.uniform(bounds[0][0], bounds[0][1]))
                random_y.append(random.uniform(bounds[1][0], bounds[1][1]))
                new_bss += [random_x[-1]] + [random_y[-1]]
            area = -1*(OptimizeLocation.objective(covered_area_by_bs, new_bss))
            if area > solution["area"]:
                solution["area"] = area
                solution["new_bss"] = new_bss
        area = -OptimizeLocation.objective(covered_area_by_bs, solution["new_bss"])
        return (OptimizeLocation.grouper(solution["new_bss"], 2), area)
