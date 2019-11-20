from itertools import chain


def enlarge_super_cell(atoms, period):
    super_cell = []
    for atom in atoms:
        type = atom.pop()
        # get possible coordinates on each axis
        x = [atom[0] + x*period[0] for x in range(-1, 2)]
        y = [atom[1] + x*period[1] for x in range(-1, 2)]
        z = [atom[2] + x*period[2] for x in range(-1, 2)]
        new_atoms = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    new_atoms.append([x[i], y[j], z[k]])
        new_atoms = [new_atom + [type] for new_atom in new_atoms]
        super_cell.append(new_atoms)
    return list(chain(*super_cell)), [period*3.0 for period in period]


if __name__ == "__main__":
    atoms = [[1.0, 1.0, 1.0, 'Ne'], [0.0, 0.0, 0.0, 'H']]
    period = [1.0, 1.0, 1.0]
    atoms, period = enlarge_super_cell(atoms, period)
    print(atoms)
    print(period)
