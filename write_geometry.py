import csv
from numpy import diag


def write_geometry(atoms, period, file):
    '''Takes a list of atoms and the period in a simple cubic cell
       and generates a geometry.in file in the AIMS style.

    Parameters:
        atoms (list): Coordinates of the atoms and types.
        period (list): 3D period of the unitcell.
        file (str): Output file name.
    '''
    for atom in atoms:
        atom.insert(0, 'atom')
    period = diag(period).tolist()
    for p in period:
        p.insert(0, 'lattice_vector')
    lattice_atoms = period + atoms
    with open(file, 'w') as out_file:
        writer = csv.writer(out_file, delimiter=' ')
        writer.writerows(lattice_atoms)


if __name__ == "__main__":
    atoms = [[0.5, 0.5, 0.5, 'Ne'], [0.0, 0.0, 0.0, 'H']]
    period = [1.0, 1.0, 1.0]

    write_geometry(atoms, period, 'geometry.out')
