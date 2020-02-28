import sys

sys.path.insert(1, "src")

from carte import *


def test_check_ship():
    carte = Carte(False)
    navire = Navire(0, 3, 1, "Calypso")
    navire.cases.append(Case(1, 2, 1))
    navire.cases.append(Case(2, 2, 1))
    navire.cases.append(Case(3, 2, 1))
    carte.navires.append(navire)

    assert carte.check_ship(2, 2, 1) == (True, False)
    assert carte.check_ship(2, 2, 2) == (False, False)
    assert carte.check_ship(2, 3, 1) == (False, False)
    assert carte.check_ship(4, 2, 1) == (False, False)


def test_positionner_navire():
    carte = Carte(False)

    carte.positionner_navire(5, 5, 1, "Vertical", "Destroyer", 0)

    assert carte.navires[0].cases[0].x == 5
    assert carte.navires[0].cases[0].y == 5
    assert carte.navires[0].cases[0].z == 1

    assert carte.navires[0].cases[1].x == 5
    assert carte.navires[0].cases[1].y == 6
    assert carte.navires[0].cases[1].z == 1

    assert carte.navires[0].cases[2].x == 5
    assert carte.navires[0].cases[2].y == 7
    assert carte.navires[0].cases[2].z == 1

    assert not carte.navires[0].cases[2].x == 6
    assert not carte.navires[0].cases[2].y == 8
    assert not carte.navires[0].cases[2].z == 2

    carte.positionner_navire(0, 0, 0, "Horizontal", "porte-container", 1)

    assert carte.navires[1].cases[9].x == 4
    assert carte.navires[1].cases[9].y == 1
    assert carte.navires[1].cases[4].y == 0

    carte.positionner_navire(0, 2, 0, "Horizontal", "Porte-avion", 2)

    assert carte.navires[2].cases[4].x == 4
    assert carte.navires[2].cases[4].y == 2
    carte.positionner_navire(6, 0, 0, "Vertical", "Torpilleur", 3)

    assert carte.navires[3].cases[5].x == 7
    assert carte.navires[3].cases[5].y == 2

    carte.positionner_navire(0, 0, 0, "Vertical", "porte-container", 4)
    carte.positionner_navire(1, 0, 0, "Vertical", "Destroyer", 4)
    carte.positionner_navire(4, 0, 0, "Horizontal", "Destroyer", 4)


def test_mise_a_jour():
    carte = Carte(False)
    carte.positionner_navire(0, 0, 0, "Vertical", "Destroyer", 0)

    carte.mise_a_jour_case(0, 0, 0)
    assert carte.cases[0].impact is True


def test_trouver_navire():
    carte = Carte(False)

    assert carte.trouver_navire(1) == "ERR"
