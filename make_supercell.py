from itertools import chain, product
from copy import deepcopy


def make_supercell(atoms, period):
    '''Takes a list of atoms and the period in a unit cell then generates
       a larger super cell

    Parameters:
        atoms (list): Coordinates of the atoms and types
        period (list): 3D period of the unit cell


    Returns:
        super_cell (list): Coordinates of atoms and types in the super cell
        period (list): Period of the super cell

    '''
    super_cell = []
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
        super_cell.append(new_atoms)
    return list(chain(*super_cell)), [period*2.0 for period in period]


def find_atom_in_origin(cell):
    raw_cell = deepcopy(cell)
    for atom in raw_cell:
        del atom[-1]

    return raw_cell.index([0.0, 0.0, 0.0])


def strip_coorners(super_cell, period):
    '''Takes a super_cell and it's period, strips the coorners that will
       be replicated by the peridicity

    Parameters:
        super_cell (list): Coordinates and atom types of contained in the super
                           cell
        period (list): 3D period of the super cell

    Returns:
        super_cell (list): Stripped down super cell
    '''
    origin = super_cell[find_atom_in_origin(super_cell)]
    type = origin[:].pop()
    coorners = [list(atom) + [type]
                for atom in list(product([0.0, period[0]], repeat=3))]
    coorners.remove([0.0, 0.0, 0.0, type])
    for coorner in coorners:
        super_cell.remove(coorner)

    return super_cell


if __name__ == "__main__":
    atoms = [[0.5, 0.5, 0.5, 'Ne'], [0.0, 0.0, 0.0, 'H']]
    period = [1.0, 1.0, 1.0]
    atoms, period = enlarge_super_cell(atoms, period)
    # print(atoms)
    atoms = strip_coorners(atoms, period)
