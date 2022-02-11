import math
from typing import TYPE_CHECKING, Optional

from indigo.exceptions import IndigoException

if TYPE_CHECKING:
    from indigo import IndigoObject

OUTER_ELECTRONS = {
    "H": 1,
    "He": 2,
    "Li": 1,
    "Be": 2,
    "B": 3,
    "C": 4,
    "N": 5,
    "O": 6,
    "F": 7,
    "Ne": 8,
    "Na": 1,
    "Mg": 2,
    "Al": 3,
    "Si": 4,
    "P": 5,
    "S": 6,
    "Cl": 7,
    "Ar": 8,
    "K": 1,
    "Ca": 2,
    "Sc": 3,
    "Ti": 4,
    "V": 5,  # 4s2 3d3 (!)
    "Cr": 6,  # 4s1 3d5 (!)
    "Mn": 7,  # 4s2 3d5
    "Fe": 8,  # 4s2 3d6
    "Co": 9,
    "Ni": 10,
    "Cu": 1,
    "Zn": 2,
    "Ga": 3,
    "Ge": 4,
    "As": 5,
    "Se": 6,
    "Br": 7,
    "Kr": 8,
    "Rb": 1,
    "Sr": 2,
    "Y": 3,  # 5s2 4d1
    "Zr": 4,  # 5s2 4d2
    "Nb": 5,  # 5s1 4d4 (!)
    "Mo": 6,  # 5s1 4d5
    "Tc": 7,  # 5s2 4d5
    "Ru": 8,  # 5s1 4d7 (!!!)
    "Rh": 9,  # 5s1 4d8
    "Pd": 10,  # 4d10 (!)
    "Ag": 1,
    "Cd": 2,
    "In": 3,
    "Sn": 4,
    "Sb": 5,
    "Te": 6,
    "I": 7,
    "Xe": 8,
    "Cs": 1,
    "Ba": 2,
    "La": 3,  # 6s2 5d1
    "Ce": 4,  # 6s2 4f2 (!!!) Atomic num = 58, lantanoids
}

N_ORBS_HYBRIDIZATION = {
    1: "unhybridized",
    2: "sp",
    3: "sp2",
    4: "sp3",
    5: "sp3d",
    6: "sp3d2",
    7: "sp3d3",
    8: "sp3d4",
}


def num_bonds(atom: "IndigoObject") -> int:
    bonds = 0
    for nei in atom.iterateNeighbors():
        bonds += nei.bond().bondOrder()
    bonds += atom.countImplicitHydrogens()
    return bonds


def has_lone_pair(atom: "IndigoObject", n_bonds: int) -> bool:
    return OUTER_ELECTRONS[atom.symbol()] - n_bonds >= 2


def lone_pairs(atom: "IndigoObject", n_bonds: int) -> int:
    outer_electrons = OUTER_ELECTRONS[atom.symbol()]
    pairs = math.floor((outer_electrons - n_bonds) / 2)
    return pairs


def cardon_hybridization(carbon: "IndigoObject") -> Optional[str]:
    neighbors = carbon.degree() + carbon.countImplicitHydrogens()
    if neighbors == 4:
        return "sp3"
    if neighbors == 3:
        return "sp2"
    if neighbors <= 2:
        return "sp"
    return None


def match_minus_induction(atom: "IndigoObject") -> bool:
    for nei in atom.iterateNeighbors():
        if nei.bond().bondOrder() == 2:
            return True
    return False


def oxygen_hybridization(oxygen: "IndigoObject") -> str:
    for nei in oxygen.iterateNeighbors():
        if nei.bond().bondOrder() == 2:
            return "sp2"
        if nei.bond().bondOrder() == 3:
            # for CO, but some sources do not recognize "sp" for oxygen
            return "sp"
        if nei.symbol() == "C" and match_minus_induction(nei):
            return "sp2"
    return "sp3"


def nitrogen_hybridization(
    nitrogen: "IndigoObject", n_bonds: int
) -> Optional[str]:
    n_orbs = nitrogen.degree() + has_lone_pair(nitrogen, n_bonds)
    minus_induction = False
    for nei in nitrogen.iterateNeighbors():
        if nei.symbol() == "C" and match_minus_induction(nei):
            minus_induction = True
    if n_orbs == 4 and minus_induction:
        return N_ORBS_HYBRIDIZATION[n_orbs - 1]
    if n_orbs <= 4:
        return N_ORBS_HYBRIDIZATION[n_orbs]
    return None


def complex_hybridization(
    atom: "IndigoObject", neighbors: int
) -> Optional[str]:
    if neighbors == 4:
        if atom.symbol() in ["Pt", "Ni", "Cu", "Au", "Pd"]:
            return "sp2d"
        return "sp3"
    if neighbors == 5:
        return "sp3d"
    if neighbors == 6:
        return "sp3d2"
    if neighbors == 7:
        return "sp3d3"
    if neighbors == 8:
        return "sp3d4"
    return None


def in_aromatic_ring(atom):
    for nei in atom.iterateNeighbors():
        if nei.bond().topology() == 10:
            return


def get_hybridization(atom: "IndigoObject") -> Optional[str]:
    """Returns hybridization string for an atom from a molecule.

    Works only with atoms with atomic numbers from 1 to 57. Don't bother with
    the lantanoids and beyond. If atom

    Args:
        atom: an indigo.IndigoObject for the atom.
    Returns:
        str: atom hybridization. Could be "s" for unhybridized atom and "sp",
        "sp2", "sp3", "sp3d", "sp3d2", "sp3d3", "sp3d4" for hybridized.
    """
    # if the atomic number is undefined or ambiguous
    if atom.atomicNumber() == 0:
        raise IndigoException("Atomic number is undefined or ambiguous")

    # don't bother with the lantanoids and beyond
    elif atom.atomicNumber() >= 57:
        raise IndigoException(
            "Hybridization is not calculated for atomic number >= 57"
        )
    if atom.atomicNumber() == 1:
        return "s"

    n_bonds = num_bonds(atom)

    if n_bonds == 0:
        return "s"

    if atom.symbol() in ["C", "N", "O", "P", "S", "B"] and in_aromatic_ring(
        atom
    ):
        return "sp2"

    if atom.atomicNumber() == 6:
        return cardon_hybridization(atom)
    if atom.atomicNumber() == 8:
        return oxygen_hybridization(atom)
    if atom.atomicNumber() == 7:
        return nitrogen_hybridization(atom, n_bonds)

    if atom.degree() >= 4:
        return complex_hybridization(atom, atom.degree())

    # number of hybridized orbitals = number of neighbours + number of lone
    # electron pairs
    # H = N + L

    n_orbs = atom.degree() + lone_pairs(atom, n_bonds)
    if n_orbs in N_ORBS_HYBRIDIZATION:
        return N_ORBS_HYBRIDIZATION[n_orbs]
    raise IndigoException("Couldn't calculate hybridization properly")
