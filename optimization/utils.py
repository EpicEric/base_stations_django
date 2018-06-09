from functools import wraps
from math import log10, sin, cos, atan2, sqrt, radians
from time import time

def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print('{} - Elapsed time: {}'.format(f.__name__, end-start))
        return result
    return wrapper

def dbsum(*args):
    sum = 0
    for arg in args:
        sum += 10**(arg/10)
    return 10 * log10(sum)

def geographic_distance(lon1, lat1, lon2, lat2):
    #https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    lon1 = radians(lon1)
    lat1 = radians(lat1)
    lon2 = radians(lon2)
    lat2 = radians(lat2)

    R = 6373.0

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def grouper(iterable, group_size):
    return list(zip(*(iter(iterable),) * group_size))
