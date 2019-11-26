from itertools import chain, product
from copy import deepcopy


def make_supercell(atoms, period):
    '''Takes a list of atoms and the period in a unitcell then generates
       a larger supercell.

    Parameters:
        atoms (list): Coordinates of the atoms and types.
        period (list): 3D period of the unitcell.


    Returns:
        supercell (list): Coordinates of atoms and types in the supercell.
        period (list): Period of the supercell.
    '''
    supercell = []
    for atom in atoms:
        type = atom.pop()
        # Get possible coordinates on each axis
        # The coordinates are shifted such that given a
        # unit cell given in the first quadrant
        # all coordinates remain positive
        x = [atom[0] + x*period[0] for x in range(3)]
        y = [atom[1] + x*period[1] for x in range(3)]
        z = [atom[2] + x*period[2] for x in range(3)]
        new_atoms = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    new_atoms.append([x[i], y[j], z[k]])
        new_atoms = [new_atom + [type] for new_atom in new_atoms]
        supercell.append(new_atoms)
    return list(chain(*supercell)), [period*2.0 for period in period]


def find_atom_in_origin(cell):
    raw_cell = deepcopy(cell)
    for atom in raw_cell:
        del atom[-1]

    return raw_cell.index([0.0, 0.0, 0.0])


def strip_coorners(supercell, period):
    '''Takes a supercell and it's period, strips the coorners that will
       be replicated by the peridicity

    Parameters:
        supercell (list): Coordinates and atom types of contained in the super
                           cell
        period (list): 3D period of the super cell

    Returns:
        supercell (list): Stripped down super cell
    '''
    origin = supercell[find_atom_in_origin(supercell)]
    type = origin[:].pop()
    coorners = [list(atom) + [type]
                for atom in list(product([0.0, period[0]], repeat=3))]
    coorners.remove([0.0, 0.0, 0.0, type])
    for coorner in coorners:
        supercell.remove(coorner)

    return supercell


def strip_external_points(supercell, period):
    '''Takes a supercell and it's period, strips points outside the unit cell.

    Parameters:
        supercell (list): Coordinates and atom types of contained in the super
                           cell
        period (list): 3D period of the super cell

    Returns:
        supercell (list): Stripped down super cell
    '''
    remove_bank = []
    for atom in supercell:
        if any(val > period[0] for val in atom[0:3]):
            remove_bank.append(atom)
    for atom in remove_bank:
        supercell.remove(atom)

    return supercell


def reduce_boundary_points(supercell, period):
    '''Takes a supercell and it's period, then removes points with containing
       the maximum coordinanate (the period) of the supercell. These points has
       to be removed since they are implicitly added when the cell is made
       periodic.

    Parameters:
        supercell (list): Coordinates and atom types of contained in the
                          supercell
        period (list): 3D period of the supercell.

    Returns:
        supercell (list): Supercell without points containing maximum boundary
                          values.
    '''

    points = []
    for atom in supercell:
        if any(val == period[0] for val in atom[0:3]):
            points.append(atom)

    for atom in points:
        supercell.remove(atom)
    return supercell


def is_cubic(lattice):
    '''Check if a lattice is cubic.'''
    import numpy as np
    lattice = np.array(lattice)
    assert lattice.shape == (3, 3),\
        f'Invalid lattice shape: {lattice.shape} is not (3, 3)'
    lattice = lattice - np.diag(np.diag(lattice))
    return np.count_nonzero(lattice - np.diag(np.diag(lattice))) == 0


if __name__ == "__main__":
    atoms = [[0.5, 0.5, 0.5, 'Ne'], [0.0, 0.0, 0.0, 'H']]
    period = [4.0, 4.0, 4.0]
    atoms, period = make_supercell(atoms, period)
    # print(atoms)
    atoms = strip_coorners(atoms, period)
    atoms = strip_external_points(atoms, period)
    atoms = reduce_boundary_points(atoms, period)
