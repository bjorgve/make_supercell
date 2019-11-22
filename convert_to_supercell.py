from make_supercell import (make_supercell, strip_external_points,
                            reduce_boundary_points)
from geometry import read_geometry, write_geometry

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()


atoms, periods = read_geometry(args.input)
atoms, periods = make_supercell(atoms, periods)
atoms = strip_external_points(atoms, periods)
atoms = reduce_boundary_points(atoms, periods)
write_geometry(atoms, periods, args.output)
