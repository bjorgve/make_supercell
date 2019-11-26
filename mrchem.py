import json
import csv
from numpy import diag
from make_supercell import is_cubic
from geometry import write_geometry, read_geometry


def read_mrchem(file):
    '''Given an mrchem.json this function extracts the atoms and the lattice
       from the input file.
    '''
    with open(file, 'r') as json_file:
        mrchem = json.load(json_file)
        atoms = [atom['xyz'] + [atom['atom'].capitalize()]
                 for atom in mrchem['molecule']['coords']]

        lattice = diag(mrchem['mra']['scaling_factor']).tolist()

    return atoms, lattice


def write_mrchem(atoms, lattice, file):
    '''Given atoms and a lattice and a template mrchem.json
       alters/adds atoms and lattice to the mrchem.json
    '''
    with open(file, 'r') as json_file:
        mrchem = json.load(json_file)

    # Clear atoms in template
    for atom in mrchem['molecule']['coords'][:]:
        mrchem['molecule']['coords'].remove(atom)

    # Add new atoms to template
    for atom in atoms:
        mrchem['molecule']['coords'].append({
            'atom': atom[-1].lower(),
            'xyz': atom[:-1]
            })

    print(lattice)
    assert is_cubic(lattice), 'Lattice must be cubic'
    mrchem['mra']['scaling_factor'] = diag(lattice).tolist()

    with open('mrchem_play.json', 'w') as output:
        mrchem = json.dump(mrchem, output, indent=2)

if __name__ == "__main__":
    atoms, lattice = read_mrchem('mrchem.json')
    write_mrchem(atoms, lattice, 'mrchem_play.json')
