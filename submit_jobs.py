"""
Submits every .submit file in the `SUBMIT` path. Makes the .sh files
executable first.
"""
import glob
import os
import subprocess

from constants import NUR, SCRIPTS_DIR

PATH = "/home/tkiet/nuradiomc"
SUBMIT = os.path.join(PATH, SCRIPTS_DIR) 

script_path = f"{'*/' if not NUR else ''}*.submit"
for fname in sorted(glob.glob(os.path.join(SUBMIT, script_path))):
    # First make executable
    subprocess.run(["chmod", "+x", fname[:-7] + ".sh"])
    # Then submit
    subprocess.run(["condor_submit", fname])

