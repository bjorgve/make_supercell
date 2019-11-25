import itertools


def make_cubic_lattice(lattice, coords_np1=[[0.0, 0.0, 0.0]],
                       coords=[]):
    '''Takes a primitive lattice and returns a simple cubic lattice and
       it's period.

    Parameters:
        lattice (list): Primitive lattice vector
        coords_np1 (list): Starting guess/newly discovered coordinates.
        coords (list): Bank of all perviously investigated coordinates.


    Returns:
        cubic cell (list): Coordinates of an atom within a cubic unit cell
        period (list): Cartesian period of the unit cell
    '''

    coords_np2 = []
    for coord in coords_np1:
        for vector in lattice:
            add = [x + y for x, y in zip(coord, vector)]
            if not in_list(coords+coords_np1+coords_np2, add):
                coords_np2.append(add)

            subtract = [x - y for x, y in zip(coord, vector)]
            if not in_list(coords+coords_np1+coords_np2, subtract):
                coords_np2.append(subtract)

    coords += coords_np1
    return_coords = coords + coords_np2
    diagonals = find_diagonals(return_coords)
    if len(diagonals) > 0:
        coorners = find_coorners(return_coords, diagonals)
        if coorners:
            return_coords = remove_negative_coordinates(return_coords)
            return_coords = remove_large_coordinates(return_coords,
                                                     coorners)
            return return_coords, [coorners, coorners, coorners]
    return make_cubic_lattice(lattice, coords_np2, coords)


def find_diagonals(coords):
    return [coord for coord in coords
            if coord[1:] == coord[:-1]
            and coord != [0.0, 0.0, 0.0]]


def in_list(coords, new_coord):
    return any(new_coord == coord for coord in coords)


def find_coorners(coords, diagonals):
    for diag in diagonals:
        possible_box = list(itertools.product([0.0, diag[0]], repeat=3))
        possible_box = [list(element) for element in possible_box]
        if all(elem
               in coords for elem in possible_box):
            return max([sublist[-1] for sublist in possible_box])
    return []


def remove_negative_coordinates(coords):
    tmp_list = [coord for coord in coords if any(val < 0.0 for val in coord)]
    for coord in tmp_list:
        coords.remove(coord)
    return coords


def remove_large_coordinates(coords, coorner):
    tmp_list = [coord for coord in coords
                if any(val > coorner for val in coord)]
    for coord in tmp_list:
        coords.remove(coord)
    return coords


if __name__ == "__main__":
    def fcc_lattice(a):
        return [[0.0, a/2.0, a/2.0],
                [a/2.0, 0.0, a/2.0],
                [a/2.0, a/2.0, 0]]

    def bcc_lattice(a):
        return [[-a/2.0, a/2.0, a/2.0],
                [a/2.0, -a/2.0, a/2.0],
                [a/2.0, a/2.0, -a/2.0]]

    fcc = fcc_lattice(4.0)
    bcc = bcc_lattice(4.0)
    print(make_cubic_lattice(fcc))
    print(make_cubic_lattice(bcc))
