import csv
from numpy import diag


def read_geometry(file):
    '''Takes a geometry.in file in the AIMS style retuns a list of the
       periodicity and the atomic coordinatesself.

    Parameters:
        file (str): Input geometry file in the AIMS style

    Returns:
        atoms (list): List of atoms with their coordinates
        perioids (list): List of 3D periodicity
    '''

    with open(file, 'r') as inp_file:
        reader = list(csv.reader(inp_file, delimiter=' '))
        lattice = reader[0:3]
        for vec in lattice:
            del vec[0]

        periods = [float(period) for period in diag(lattice)]

        atoms = reader[3:]
        for atom in atoms:
            del atom[0]
        for atom in atoms:
            for i, coord in enumerate(atom):
                try:
                    atom[i] = float(coord)
                except ValueError:
                    None
        return atoms, periods


if __name__ == "__main__":
    atoms, periods = read_geometry('geometry.in')
    print(atoms)
    print(periods)
