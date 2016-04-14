#!/usr/bin/python
# coding=utf-8

from __future__ import division, print_function, unicode_literals

import data
import plotting
import numpy as np

datasets = data.ensure()

for name, dataset in datasets.items():
    plotting.vector_field(
        dataset["positions"]["x"],
        dataset["positions"]["y"],
        dataset["positions"]["z"],
        dataset["positions"]["u"],
        dataset["positions"]["v"],
        dataset["positions"]["w"],
        name=name,
    )

from mayavi import mlab
mlab.show()