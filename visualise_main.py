#!/usr/bin/python
# coding=utf-8

from __future__ import division, print_function, unicode_literals

import data
import plotting
import numpy as np

datasets = data.ensure_by_type()

colors = {
    'normal': (0, 0, 1), # Blue
    'thrust': (1, 0, 0), # Red
    'ambiguous': (0.75, 0.75, 0), # Yellow
    'unknown': (0, 0, 0), # Black
    'other': (0, 1, 0), # Green
}

for name, dataset in datasets.items():
    for shear_sense, shear_sense_dataset in dataset.items():
        plotting.vector_field(
            shear_sense_dataset["positions"]["x"],
            shear_sense_dataset["positions"]["y"],
            shear_sense_dataset["positions"]["z"],
            shear_sense_dataset["positions"]["u"],
            shear_sense_dataset["positions"]["v"],
            shear_sense_dataset["positions"]["w"],
            name=name,
            constant_color=colors[shear_sense],
        )

from mayavi import mlab
mlab.show()