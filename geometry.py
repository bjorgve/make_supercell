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

    write_geometry(atoms, period, 'test_geometry.out')

    atoms, periods = read_geometry('test_geometry.in')
    print(atoms)
    print(periods)
