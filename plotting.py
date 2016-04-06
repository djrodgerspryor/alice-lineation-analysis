# coding=utf-8

from __future__ import division, print_function, unicode_literals

import numpy as np

import os

os.environ["ETS_TOOLKIT"] = "qt4"
from mayavi import mlab
mlab.options.backend = 'envisage'

def vector_field(*args):
    figure = mlab.figure(
        'Lineation Field',
        fgcolor=(0, 0, 0),
        bgcolor=(1, 1, 1)
    )

    mlab.quiver3d(*args, line_width=3, scale_factor=1, figure=figure)

def show():
    """
        Enters the main render-loop for the visualisation (so that it stays on screen
        at the end of a script).
    """

    mlab.show()