#!/bin/sh
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh`
export PYTHONPATH=/home/tkiet/NuRadioMC:
python T01generate_event_list.py
