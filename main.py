#!/usr/bin/python
# coding=utf-8

from __future__ import division, print_function, unicode_literals

import data
import plotting
import numpy as np

dataset = data.load()

plotting.vector_field(
    dataset["positions"]["x"],
    dataset["positions"]["y"],
    dataset["positions"]["z"],
    lambda x, y, z: [
        4 * x**2 / np.linalg.norm([x, y, z]),
        4 * 2*y / np.linalg.norm([x, y, z]),
        4 * -z / np.linalg.norm([x, y, z]),
    ]
)

from mayavi import mlab
mlab.show()