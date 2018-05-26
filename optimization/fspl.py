from math import log10
from .utils import geographic_distance, dbsum

def free_space_path_loss(distance, frequency):
    return 20 * log10(distance) + 20 * log10(frequency) - 147.55

def objective(current_bss_list, new_bss):
    frequency = 1800 * 10**6
    total_path_loss = 0
    for bss in current_bss_list:
        distance = geographic_distance(bss.point.x, bss.point.y, new_bss[0], new_bss[1])
        path_loss = free_space_path_loss(distance, frequency)
        total_path_loss = dbsum(total_path_loss, path_loss)
        print(total_path_loss)
    return total_path_loss
    