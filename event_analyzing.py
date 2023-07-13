
from __future__ import absolute_import, division, print_function
import numpy as np
from radiotools import helper as hp
from radiotools import plthelpers as php
from matplotlib import pyplot as plt
from NuRadioReco.utilities import units
import h5py
import argparse
import json
import time
import os

parser = argparse.ArgumentParser(description='Plot NuRadioMC event list input')
parser.add_argument('inputfilename', type=str, nargs='+',
                    help='path to NuRadioMC hdf5 simulation input')
args = parser.parse_args()

# data for vertex plot
xx = []
yy = []
zz = []
zeniths = []
azimuths = []
inelasticity = []
flavors = []
interaction_type = []

filename = os.path.splitext(os.path.basename(args.inputfilename[0]))[0]
dirname = os.path.dirname(args.inputfilename[0])

for input_filename in args.inputfilename:
    print(f"parsing file {input_filename}")
    fin = h5py.File(input_filename, 'r')
    xx.extend(np.array(fin['xx']))
    yy.extend(np.array(fin['yy']))
    zz.extend(np.array(fin['zz']))
    zeniths.extend(np.array(fin['zeniths']))
    azimuths.extend(np.array(fin['azimuths']))
    inelasticity.extend(np.array(fin['inelasticity']))
    flavors.extend(np.array(fin['flavors']))
    interaction_type.extend(np.array(fin['interaction_type']))

print("number of events:", len(xx))
print("flavors:",plt.hist(flavors ))
