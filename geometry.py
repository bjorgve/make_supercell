import csv
from numpy import diag


def read_geometry(file):
    '''Takes a geometry.in file in the AIMS style retuns a list of the
       periodicity and the atomic coordinates.

    Parameters:
        file (str): Input geometry file in the AIMS style

    Returns:
        atoms (list): List of atoms with their coordinates.
        lattice (list): Lattice vector.
    '''

    with open(file, 'r') as inp_file:
        reader = list(csv.reader(inp_file, delimiter=' '))
        lattice = reader[0:3]

        # Remove 'lattice vector'
        for vec in lattice:
            assert vec[0] == 'lattice_vector',\
                f'Line should start with lattice_vector not {vec[0]}'
            del vec[0]
        lattice = [[float(nr) for nr in row] for row in lattice]

        # Remove 'atom'
        atoms = reader[3:]
        for atom in atoms:
            assert atom[0] == 'atom',\
                f'Line should start with atom not {atom[0]}'
            del atom[0]

        # Convert string numbers to floats
        for atom in atoms:
            for i, coord in enumerate(atom):
                try:
                    atom[i] = float(coord)
                except ValueError:
                    None
        return atoms, lattice


def write_geometry(atoms, lattice, file):
    '''Takes a list of atoms and a lattice vector and generates a geometry.in
       file in the AIMS style.

    Parameters:
        atoms (list): Coordinates of the atoms and types.
        lattice (list): 3D lattice vector.
        file (str): Output file name.
    '''
    for atom in atoms:
        atom.insert(0, 'atom')

    for p in lattice:
        p.insert(0, 'lattice_vector')
    lattice_atoms = lattice + atoms
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
