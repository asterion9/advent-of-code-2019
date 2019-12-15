import logging
import sys

import day06_input

input_orbits = day06_input.input_string.split("\n")


def build_tree(orbits: list):
    orbit_tree = dict()
    centers = dict()
    for orbit in orbits:
        center, astre = orbit.split(")")
        centers[astre] = center
        if astre not in orbit_tree:
            orbit_tree[astre] = set()
        if center not in orbit_tree:
            orbit_tree[center] = set()
        orbit_tree[center].add(astre)
    return orbit_tree, centers


def count_orbit(orbit_tree, cur_orbit, orbit_level):
    logging.debug(f"{cur_orbit}")
    return orbit_level + sum((count_orbit(orbit_tree, astre, orbit_level + 1) for astre in orbit_tree[cur_orbit]))


def exo1():
    orbits_tree = build_tree(input_orbits)[0]
    return count_orbit(orbits_tree, "COM", 0)


def build_parents(centers, astre):
    if astre not in centers:
        return [astre]
    else:
        return build_parents(centers, centers[astre]) + [astre]


def exo2():
    centers = build_tree(input_orbits)[1]
    my_parents = build_parents(centers, "YOU")
    target_parents = build_parents(centers, "SAN")
    for parent in reversed(my_parents):
        if parent in target_parents:
            return (len(my_parents) - 1 - my_parents.index(parent) - 1) \
                   + (len(target_parents) - 1 - target_parents.index(parent) - 1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sys.setrecursionlimit(10000)
    print(exo2())
