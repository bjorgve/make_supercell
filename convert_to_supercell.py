from make_supercell import make_supercell, strip_coorners
from write_geometry import write_geometry
from read_geometry import read_geometry

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()


atoms, periods = read_geometry(args.input)
atoms, periods = make_supercell(atoms, periods)
atoms = strip_coorners(atoms, periods)
write_geometry(atoms, periods, args.output)
