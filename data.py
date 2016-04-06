# coding=utf-8

from __future__ import division, print_function, unicode_literals

import numpy as np

def load():
    x, y, z = np.mgrid[-2:3, -2:3, -2:3]

    return {
        "positions": {
            "x": x,
            "y": y,
            "z": z,
        },
    }