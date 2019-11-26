from make_supercell import (make_supercell, strip_external_points,
                            reduce_boundary_points, is_cubic)
from geometry import read_geometry, write_geometry

import argparse
import numpy as np

'''Convert a cubic unitcell to a supercell.'''

parser = argparse.ArgumentParser()

parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()


atoms, lattice = read_geometry(args.input)
assert is_cubic(lattice), 'Lattice must be cubic'
periods = np.diag(lattice).tolist()
atoms, periods = make_supercell(atoms, periods)
print(atoms)
atoms = strip_external_points(atoms, periods)
atoms = reduce_boundary_points(atoms, periods)

# Making lattice
periods = np.diag(periods).tolist()
write_geometry(atoms, periods, args.output)
