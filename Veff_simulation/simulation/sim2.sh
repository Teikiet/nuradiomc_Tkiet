#!/bin/sh
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh`
export PYTHONPATH=/home/tkiet/NuRadioMC:
python T02RunSimulation.py event_file/1e19_n1e4.hdf5 surface_station_1GHz.json config.yaml output/output_1e19_n1e4.hdf5
