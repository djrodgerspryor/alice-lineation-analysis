#!/usr/bin/python
# coding=utf-8

from __future__ import division, print_function, unicode_literals

import data
import numpy as np
#from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import math
from surf2solid import surf2solid

SIDE_LENGTH = 700
BORDER = 0.1
MODEL_SIZE_MM = 80

datasets = data.ensure_array()

name = '8 - Pelling, Hee and Yuksom'
dataset = datasets[name]

# Create a new plot
#figure = plt.figure()
#axes = mplot3d.Axes3D(figure)
fig, axs = plt.subplots(1, 1, figsize=(10, 10))

data = np.zeros((SIDE_LENGTH, SIDE_LENGTH), dtype='float')

x_min = min(datapoint['x'] for datapoint in dataset)
x_max = max(datapoint['x'] for datapoint in dataset)
y_min = min(datapoint['y'] for datapoint in dataset)
y_max = max(datapoint['y'] for datapoint in dataset)

x_range = x_max - x_min
y_range = y_max - y_min

x_max += x_range * BORDER
x_min -= x_range * BORDER

y_max += y_range * BORDER
y_min -= y_range * BORDER

def calc_z(x, y, **kwargs):
    nearest = None
    nearest_r = None
    for datapoint in dataset:
        r = math.sqrt((x - datapoint['x'])**2 + (y - datapoint['y'])**2)

        if nearest is None or r < nearest_r:
            nearest = datapoint
            nearest_r = r

    base_height = nearest['z']

    x_diff = x - nearest['x']
    y_diff = y - nearest['y']

    dot_product = (x_diff * nearest['u']) + (y_diff * nearest['v'])

    return base_height + (dot_product * nearest['w'])


x_list, y_list, z_list = [], [], []

points = {}
for i, x in enumerate(np.linspace(x_min, x_max, SIDE_LENGTH)):
    points[i] = {}

    for j, y in enumerate(np.linspace(y_min, y_max, SIDE_LENGTH)):
        z = calc_z(x, y)
        data[i, j] = z

        x_list.append(x)
        y_list.append(y)
        z_list.append(z)

if x_range > y_range:
    size = (MODEL_SIZE_MM, MODEL_SIZE_MM * (y_range / x_range))
else:
    size = (MODEL_SIZE_MM * (x_range / y_range), MODEL_SIZE_MM)

z_min = np.min(data)
z_max = np.max(data)
z_range = z_max - z_min

surf2solid(
    calc_z,
    name,
    x_min=x_min,
    x_max=x_max,
    y_min=y_min,
    y_max=y_max,
    z_min=z_min - (z_range * BORDER),
    size=size,
    resolution=SIDE_LENGTH,
)


axs.imshow(data, cmap='seismic', interpolation='none')


#fig3d = plt.figure()
#ax3d = fig3d.add_subplot(111, projection='3d')
#from matplotlib.tri.triangulation import Triangulation
#triangles, _, _ = Triangulation.get_from_args_and_kwargs(x_list, y_list, z_list)
#print(triangles.triangles)
#ax3d.plot_trisurf(x_list, y_list, z_list, cmap='seismic')

plt.show()