"""
Runs a simulation.
"""
import argparse
import os

from constants import NUR
from simulate import Simulation

parser = argparse.ArgumentParser(description='Run a simulation for a specific event file.')
parser.add_argument('inputfilename', type=str)
parser.add_argument('outputfilename', type=str)
if NUR:
    parser.add_argument('outputfilenameNuRadioReco', type=str)
parser.add_argument('detectorfile', type=str)
parser.add_argument('configfile', type=str)
args = parser.parse_args()

sim = Simulation(
    inputfilename=args.inputfilename,
    outputfilename=args.outputfilename,
    outputfilenameNuRadioReco=None if not NUR else args.outputfilenameNuRadioReco,
    detectorfile=args.detectorfile,
    config_file=args.configfile,
    file_overwrite=True,
)
sim.run()
