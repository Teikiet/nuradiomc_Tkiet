#!/bin/sh
eval "$(/cvmfs/icecube.opensciencegrid.org/users/gen2-radio-sim/tools/miniconda/bin/conda shell.bash hook)"
export PYTHONPATH=/home/tkiet/NuRadioMC:
python /home/tkiet/nuradiomc/Correlation/correlation.py
