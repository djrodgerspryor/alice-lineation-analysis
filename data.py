# coding=utf-8

from __future__ import division, print_function, unicode_literals

import numpy as np
import math

import sys
sys.path.insert(0, 'data')

import load

# Radius of earth in meters
earth_radius = 6.3674447*(10**6)

vec_scale = 500

def latlong_to_meters(lat1, long1, lat2, long2):
    phi1 = math.radians(90.0 - lat1)
    phi2 = math.radians(90.0 - lat2)

    theta1 = math.radians(long1)
    theta2 = math.radians(long2)

    cos = (
        math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
        math.cos(phi1) * math.cos(phi2)
    )
    arc = math.acos(cos)

    r = arc * earth_radius

    deltaPhi = phi1 - phi2
    deltaTheta = theta2 - theta1

    y = math.sin(theta2 - theta1) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(theta2 - theta1)
    bearing = -math.atan2(y, x)

    return [math.sin(bearing) * r, math.cos(bearing) * r]

def dataset2arraysbytype(dataset):
    mean_lat = np.mean([datapoint['lat'] for datapoint in dataset])
    mean_long = np.mean([datapoint['long'] for datapoint in dataset])

    result = {}

    for shear_sense in set(datapoint['shear-sense'] for datapoint in dataset):
        x, y, z, u, v, w = [], [], [], [], [], []
        for datapoint in dataset:
            if datapoint['shear-sense'] == shear_sense:
                _x, _y = latlong_to_meters(datapoint['lat'], datapoint['long'], mean_lat, mean_long)
                x.append(_x)
                y.append(_y)

                z.append(datapoint['elevation'])
                u.append(datapoint['u'] * vec_scale)
                v.append(datapoint['v'] * vec_scale)
                w.append(datapoint['w'] * vec_scale)

        result[shear_sense] = {
            "positions": {
                "x": np.array(x),
                "y": np.array(y),
                "z": np.array(z),
                "u": np.array(u),
                "v": np.array(v),
                "w": np.array(w),
            },
        }

    return result

def dataset2array(dataset):
    mean_lat = np.mean([datapoint['lat'] for datapoint in dataset])
    mean_long = np.mean([datapoint['long'] for datapoint in dataset])

    results = []
    for datapoint in dataset:
        _x, _y = latlong_to_meters(datapoint['lat'], datapoint['long'], mean_lat, mean_long)

        results.append({
            'x': _x,
            'y': _y,
            'z': datapoint['elevation'],
            'u': datapoint['u'],
            'v': datapoint['v'],
            'w': datapoint['w'],
        })

    return results

def ensure_array():
    result = {}

    for k, dataset in load.datasets_by_file.items():
        result[k] = dataset2array(dataset)

    return result

def ensure_by_type():
    result = {}

    for k, dataset in load.datasets_by_file.items():
        result[k] = dataset2arraysbytype(dataset)

    return result
