# coding=utf-8

from __future__ import division, print_function, unicode_literals

import numpy as np
import os
import glob
import math
import ntpath
import codecs

heading_map = {
    "Area": "area",
    "Site #": "stite-id",
    "Latitude": "lat",
    "Longitude": "long",
    "elevation (m)": "elevation",
    "Rock description": "rock-description",
    "Soimplified rock type": "rock-type",
    "Ls direction": "ls-direction",
    "Ls plunge": "ls-plunge",
}

required_headings = ['lat', 'long', 'elevation', 'ls-direction', 'ls-plunge']

def map_heading(heading):
    return heading_map.get(heading, heading)

datasets_by_file = {}

for fname in glob.glob(os.path.dirname(os.path.realpath(__file__)) + '/*.csv'):
    print("Opening", fname)

    dataset = []

    with codecs.open(fname, encoding='utf8') as fp:
        headings = [map_heading(heading.strip()) for heading in fp.readline().split(',')]

        for line in fp:
            data = dict(zip(headings, [value for value in line.split(',')]))

            if all(data[heading] for heading in required_headings):
                data['lat'] = float(data['lat'])
                data['long'] = float(data['long'])
                data['elevation'] = float(data['elevation'])

                data['ls-direction-rad'] = math.radians(float(data['ls-direction']))
                data['ls-plunge-rad'] = math.radians(float(data['ls-plunge']))

                data['u'] = math.cos(float(data['ls-direction-rad']))
                data['v'] = math.sin(float(data['ls-direction-rad']))
                data['w'] = math.sin(-float(data['ls-plunge-rad']))

                dataset.append(data)

    datasets_by_file[ntpath.basename(fname).replace('.csv', '')] = dataset