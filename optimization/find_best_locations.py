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
        bs_objects = [OptimizedBaseStation(point = Point(bs[0], bs[1]))
                    for bs in OptimizeLocation.grouper(new_bss, 2)]
        # print("NEW_BSS:", bs_objects[0].point)
        new_bss_covered_area = map(lambda bs: bs.covered_area, bs_objects)
        new_bss_union = reduce(lambda bs0, bs1: bs0 | bs1, new_bss_covered_area)
        bss_union = reduce(lambda x, y: x | y, covered_area_by_bs)
        # print("AREA_BSS:",bss_union.area)
        # print("NEW_AREA:", new_bss_union.area)
        # print("SUM", bss_union.area+new_bss_union.area)
        total_area = (new_bss_union | bss_union).area
        # print(total_area)
        return -(total_area)

    def basinhopping(base_stations, number, bounds):
        x0 = []
        for i in range (0, number):
            x = random.uniform(bounds[0][0], bounds[0][1])
            y = random.uniform(bounds[1][0], bounds[1][1])
            x0.append(Point(x, y))

        minimizer_kwargs = {"method":"SLSQP", "bounds": bounds * number}
        covered_area_by_bs = list(map(lambda bs: bs.covered_area, base_stations))
        solution = basinhopping(lambda x: OptimizeLocation.objective(covered_area_by_bs, x), x0, minimizer_kwargs=minimizer_kwargs,
                    niter=10, disp=True, stepsize=1/50)
        # print(solution.x)
        return OptimizeLocation.grouper(solution.x, 2)

    def slsqp(base_stations, number, bounds):
        x = random.uniform(bounds[0][0], bounds[0][1])
        y = random.uniform(bounds[1][0], bounds[1][1])
        x0 = []
        for i in range (0, number):
            x0.append(Point(x, y))

        covered_area_by_bs = list(map(lambda bs: bs.covered_area, base_stations))

        solution = minimize(lambda bss: OptimizeLocation.objective(covered_area_by_bs, bss),
                            x0,
                            method='SLSQP',
                            bounds=bounds * number,
                            options={'eps': 1.4901161193847656e-04, "disp": True, 'ftol': 1e-12})
        return OptimizeLocation.grouper(solution.x, 2)

    def taguchi(base_stations, number, bounds):
        x = (bounds[0][1] - bounds[0][0])/2 + bounds[0][0]
        y = (bounds[1][1] - bounds[1][0])/2 + bounds[1][0]
        x0 = []
        for i in range (0, number):
            x0.append(Point(x, y))

        covered_area_by_bs = list(map(lambda bs: bs.covered_area, base_stations))
        solution = taguchi(bounds * number, 3, lambda bss: OptimizeLocation.objective(covered_area_by_bs, bss), 0.95)
        return OptimizeLocation.grouper(solution['x'], 2)

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
        # print(area)
        return OptimizeLocation.grouper(solution["new_bss"], 2)
