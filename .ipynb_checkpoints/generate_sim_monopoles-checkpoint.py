"""
Creates the .sh and .submit files necessary for submitting jobs in the condor cluster.
There is exactly one .sh and .submit file for each hdf5 event file to spread across CPUs.
"""
import glob
import os

from constants import NUR, DET_FILE, EVTS_DIR, SIMS_DIR, SCRIPTS_DIR, DETECTOR, CONFIG


def _mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

PATH2 = "/data/user/tkiet/finish_sims"
PATH3 = "/data/user/tkiet/events_monopoles"
PATH = os.environ['NURADIOMC_WORKDIR'] 
#os.path.join(PATH, DET_FILE)
INPUT = os.path.join(PATH3, EVTS_DIR)
OUTPUT = os.path.join(PATH2, SIMS_DIR) 
SCRIPTS = os.path.join(PATH, SCRIPTS_DIR) 

# Make directories if they don't already exist
_mkdir(OUTPUT)
_mkdir(SCRIPTS)


# Grab every hdf5.partXXXX file, sorted, and iterate through them
#file_format = f"{'*/' if not NUR else ''}*.hdf5{'.*' if not NUR else ''}"
file_format = f"{'*/'}*.hdf5{'.*'}"
for fname in sorted(glob.glob(os.path.join(INPUT, file_format))):
    current_dir = os.path.split(os.path.dirname(fname))[-1]

    # Simulation output is identical to event ouput except evt --> sim
    if NUR:
        #outputfilename = os.path.join(OUTPUT, os.path.basename(fname).replace("evt", "sim")) 
        #outputfilenameNuRadioReco = outputfilename.replace("hdf5", "nur")
        outputfilename = os.path.join(OUTPUT, current_dir, os.path.basename(fname).replace("evt", "sim")) 
        outputfilenameNuRadioReco = outputfilename.replace("hdf5", "nur")
    else:
        outputfilename = os.path.join(OUTPUT, current_dir, os.path.basename(fname).replace("evt", "sim")) 
    pyname = os.path.join(PATH, "run_simulation.py")

    # Command to run in .sh file
    cmd = f"export PYTHONPATH={os.environ['PYTHONPATH']}\n"
    cmd += f"python {pyname} {fname} {outputfilename} {'' if not NUR else outputfilenameNuRadioReco} {DETECTOR} {CONFIG}\n"
    header = "#!/bin/sh\n"
    # Setup python environment (currently python 3.7)
    header += "eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh`\n" 

    # Create directory for .sh and .submit files and write script files 
    if NUR:
        #current_sh_dir = SCRIPTS
        current_sh_dir = os.path.join(SCRIPTS, current_dir)
        _mkdir(current_sh_dir)
    else:
        current_sh_dir = os.path.join(SCRIPTS, current_dir)
        _mkdir(current_sh_dir)
    sh_name = os.path.join(current_sh_dir, os.path.basename(fname) + ".sh")
    with open(sh_name, "w") as f:
        f.write(header)
        f.write(cmd)

    data = f"executable = {sh_name}\n" 
    data += f"log = {sh_name[:-2] + 'log'}\n"
    data += f"output = {sh_name[:-2] + 'out'}\n"
    data += f"error = {sh_name[:-2] + 'err'}\n"
    data += "request_memory = 15GB\n\n"
    data += "queue 1\n"

    # and now write .submit files
    with open(os.path.join(current_sh_dir, os.path.basename(fname) + ".submit"), "w") as f:
        f.write(data)

