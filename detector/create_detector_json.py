"""
Creates JSON detector files for NuRadioMC simulation of various forms.
"""
import sys

from constants import DET_NAME
from detector import Detector

def get_cube_coords(x, y, z, length):
    """
    Centers a cube of length `length` around coordinate (`x`, `y`, `z`).
    """
    return [
        [x + length / 2, y + length / 2, z + length / 2],
        [x + length / 2, y + length / 2, z - length / 2],
        [x + length / 2, y - length / 2, z + length / 2],
        [x + length / 2, y - length / 2, z - length / 2],
        [x - length / 2, y + length / 2, z + length / 2],
        [x - length / 2, y + length / 2, z - length / 2],
        [x - length / 2, y - length / 2, z + length / 2],
        [x - length / 2, y - length / 2, z - length / 2]
    ]

def staggered_cube(t_antenna, t_orien, t_rot, b_antenna, b_orien, b_rot, coord=[0, 0, -200], length=20, offset=1, name=None):
    """
    A total of 16 antennas in the form of two cubes (marking their vertices) offset vertically
    but otherwise identically in the x and y directions.

    Parameters:
    t_antenna: The antenna that makes up the higher cube and is centered on `coord`.
    t_orien: The two orientation angles for the 8 `t_antenna`'s.
    t_rot: The two rotation angles for the 8 `t_antenna`'s.
    b_antenna: The antenna that makes up the lower cube and is vertically offset by
        `offset` meters from the cube made of the `t_antenna` antennas.
    b_orien: The two orientation angles for the 8 `b_antenna`'s.
    b_rot: The two rotation angles for the 8 `b_antenna`'s.
    coord (default [0, 0, -200]): The coordinates that the higher cube is centered on.
    length (default 20): The length of the sides of the cube.
    offset (default 1): The vertical offset between the two cubes.
    name (default None): Name of the JSON file. Specially `name`_detector.json. If none
        is given, it defaults to the value DET_NAME from constants.py.
    """
    det = Detector()
    det.station_default()

    t_coords = get_cube_coords(*coord, length)
    b_coords = get_cube_coords(*[coord[0], coord[1], coord[2] - offset], length)
    for t_coord in t_coords:
        det.create_channel(
            t_antenna,
            t_coord[0],
            t_coord[1],
            t_coord[2],
            {"theta": t_orien[0], "phi": t_orien[1]},
            {"theta": t_rot[0], "phi": t_rot[1]}
        )
    for b_coord in b_coords:
        det.create_channel(
            b_antenna,
            b_coord[0],
            b_coord[1],
            b_coord[2],
            {"theta": b_orien[0], "phi": b_orien[1]},
            {"theta": b_rot[0], "phi": b_rot[1]}
        )
    det.create_json(f"{DET_NAME if name is None else name}_detector")

def cube(antenna, orien, rot, coord=[0, 0, -200], length=20, name=None):
    """
    A cube where the antennas make up the 8 vertices.

    Parameters:
    antenna: The antenna that makes up the cube.
    orien: The two orientation angles for the antennas.
    rot: The two rotation angles for the antennas.
    coord (default [0, 0, -200]): The coordinates that the cube is centered on.
    length (default 20): The length of the sides of the cube.
    name (default None): Name of the JSON file. Specially `name`_detector.json. If none
        is given, it defaults to the value DET_NAME from constants.py.
    """
    det = Detector()
    det.station_default()

    coords = get_cube_coords(*coord, length)
    for det_coord in coords:
        det.create_channel(
            antenna,
            det_coord[0],
            det_coord[1],
            det_coord[2],
            {"theta": orien[0], "phi": orien[1]},
            {"theta": rot[0], "phi": rot[1]} 
        )
    det.create_json(f"{DET_NAME if name is None else name}_detector")

def single(antenna, orien, rot, coord=[0, 0, -200], name=None):
    """
    A single detector.

    Parameters:
    antenna: The name of the antenna used.
    orien: The two orientation angles for the antenna.
    rot: The two rot angles for the antenna.
    coord (default [0, 0, -200]): The coordinates the antenna is located.
    name (default None): Name of the JSON file. Specially `name`_detector.json. If none
        is given, it defaults to the value DET_NAME from constants.py.
    """
    det = Detector()
    det.station_default()

    det.create_channel(
        antenna,
        coord[0],
        coord[1],
        coord[2],
        {"theta": orien[0], "phi": orien[1]},
        {"theta": rot[0], "phi": rot[1]},
    )
    det.create_json(f"{DET_NAME if name is None else name}_detector")


if __name__ == "__main__":
    dipole, bicone = 'dipole_z_z90', 'bicone2020_13z'
    hpol, vpol = 'RNOG_quadslot_v2_n1.74', 'RNOG_vpol_4inch_center_n1.73'
    dtype = sys.argv[1]
    # Singles
    if dtype == 'single_v_dipole':
        single(dipole, (0, 0), (90, 0), name=dtype)
    elif dtype == 'single_h_dipole':
        single(dipole, (90, 0), (0, 0), name=dtype)
    elif dtype == 'single_v_bicone':
        single(bicone, (0, 0), (90, 0), name=dtype)
    elif dtype == 'single_h_bicone':
        single(bicone, (90, 0), (0, 0), name=dtype)
    # Cubes
    elif dtype == 'cube_v_dipole':
        cube(dipole, (0, 0), (90, 0), name=dtype)
    elif dtype == 'cube_h_dipole':
        cube(dipole, (90, 0), (0, 0), name=dtype)
    elif dtype == 'cube_v_bicone':
        cube(bicone, (0, 0), (90, 0), name=dtype)
    elif dtype == 'cube_h_bicone':
        cube(bicone, (90, 0), (0, 0), name=dtype)
    elif dtype == 'cube_quadslot':
        cube(hpol, (0, 0), (90, 0), name=dtype)
    elif dtype == 'cube_vpol':
        cube(vpol, (0, 0), (90, 0), name=dtype)
    # Staggered Cubes
    elif dtype == 'staggered_h_bicone':
        staggered_cube(bicone, (90, 0), (0, 0), vpol, (0, 0), (90, 0), name=dtype)
    elif dtype == 'staggered_v_bicone':
        staggered_cube(bicone, (0, 0), (90, 0), vpol, (0, 0), (90, 0), name=dtype)
    elif dtype == 'staggered_h_dipole':
        staggered_cube(dipole, (90, 0), (0, 0), vpol, (0, 0), (90, 0), name=dtype)
    elif dtype == 'staggered_v_dipole':
        staggered_cube(dipole, (0, 0), (90, 0), vpol, (0, 0), (90, 0), name=dtype)
    elif dtype == 'staggered_quadslot':
        staggered_cube(hpol, (0, 0), (90, 0), vpol, (0, 0), (90, 0), name=dtype)
    else:
        print(f"No dtype '{dtype}' available.")
