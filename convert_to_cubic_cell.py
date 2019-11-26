from make_cubic_lattice import make_cubic_lattice
from make_supercell import is_cubic, reduce_boundary_points
from geometry import read_geometry, write_geometry

import argparse
import numpy as np

'''Convert a primitive lattice to a simple cubic unit cell'''

parser = argparse.ArgumentParser()

parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()

atoms, lattice = read_geometry(args.input)
assert not is_cubic(lattice), 'Lattice is already cubic'
element = atoms[0][-1]
atoms, period = make_cubic_lattice(lattice)
atoms = [atom + [element] for atom in atoms]
atoms = reduce_boundary_points(atoms, period)

lattice = np.diag(period).tolist()
write_geometry(atoms, lattice, args.output)
