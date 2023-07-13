"""
Generates events. There are `NUM_EVENTS` logarithmetically equidistant energies. A directory
indicating the number of events per energy, number of energy levels and the max and min of the
energy (`evts_path` below). In that, there are subdirectories which indicate each energy and
contain the .hdf5.partXXXX files for each respective energy.
"""
import os

import numpy as np
from NuRadioMC.EvtGen.generator import generate_eventlist_cylinder, generate_monopoles, generate_surface_muons
from NuRadioReco.utilities import units
E_min = 1e16
E_max = 1e18
N = 1
VOLUME = {
    "fiducial_zmin": -2.7 * units.km,
    "fiducial_zmax": 0,
    "fiducial_rmin": 0,
    "fiducial_rmax": 3 * units.km
}

generate_monopoles(
       ' monopoles.hdf5',
        n_events=N,
        Emin=E_min * units.eV,
        Emax=E_max * units.eV,
        volume=VOLUME
    )
generate_surface_muons(
        'muon.hdf5',
        n_events=N,
        Emin=E_min * units.eV,
        Emax=E_max * units.eV, 
        volume=VOLUME
    )

