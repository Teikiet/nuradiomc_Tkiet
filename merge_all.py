"""
Uses `merge_hdf5.py` on all simulation directories in the given input directory
and moves them into the given output directory. Leaves the original directories
of unmerged hdf5s unchanged.
"""
import glob
import os
import shutil
import subprocess
import sys

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    sim_dirs = os.listdir(input_path)

    print(f"Merging HDF5 files from {input_path}")
    print(f"Merging {len(sim_dirs)} different simulations.")
    print(f"Moving merged HDF5 files to {output_path}")

    os.mkdir(output_path)
    for sim_dir in sim_dirs:
        input_dir = os.path.join(input_path, sim_dir)
        output_dir = os.path.join(output_path, sim_dir)

        subprocess.run(["python", "merge_hdf5.py", input_dir])
        os.mkdir(output_dir)
        for hdf5 in glob.glob(os.path.join(input_dir, "*.hdf5")):
            shutil.move(hdf5, os.path.join(output_dir, os.path.basename(hdf5)))

        print(f"Merged files from {input_dir} and placed in {output_dir}")
