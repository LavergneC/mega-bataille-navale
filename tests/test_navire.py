import sys

sys.path.insert(1, "src")

from navire import *


def test_test_impact():
    navire = Navire(0, 3, 1, "Calypso")
    navire.cases.append(Case(1, 2, 1))
    navire.cases.append(Case(2, 2, 1))
    navire.cases.append(Case(3, 2, 1))

    assert navire.test_impact(4, 2, 1)[1] is False
    assert navire.test_impact(2, 2, 1)[1] is True

    assert navire.test_impact(1, 1, 1)[1] is False
    assert navire.test_impact(2, 2, 2)[1] is False

    assert navire.test_impact(-2, 2, 1)[1] is False
    assert navire.test_impact(2.2, 2, 1)[1] is False


def test_set_position():
    navire = Navire(0, 3, 1, "Calypso")
    navire.set_position(5, 5, 1, "Vertical")

    assert navire.cases[0].x == 5
    assert navire.cases[0].y == 5
    assert navire.cases[0].z == 1

    assert navire.cases[1].x == 5
    assert navire.cases[1].y == 6
    assert navire.cases[1].z == 1

    assert navire.cases[2].x == 5
    assert navire.cases[2].y == 7
    assert navire.cases[2].z == 1

    assert not navire.cases[2].x == 6
    assert not navire.cases[2].y == 8
    assert not navire.cases[1].z == 2

    navire2 = Navire(1, 3, 1, "Antargaz")
    navire2.set_position(1, 3, 2, "Horizontal")

    assert navire2.cases[0].x == 1
    assert navire2.cases[0].y == 3
    assert not navire2.cases[0].x == 2

    assert navire2.cases[2].x == 3
    assert navire2.cases[2].y == 3
    assert not navire2.cases[2].y == 4


def test_contient_case():
    navire = Navire(1, 3, 2, "Bat")
    navire.set_position(0, 0, 1, "Horizontal")

    assert navire.contient_case(0, 0, 1) is True
    assert navire.contient_case(0, 1, 1) is True
    assert navire.contient_case(1, 0, 1) is True
    assert navire.contient_case(2, 0, 1) is True
    assert navire.contient_case(2, 1, 1) is True
    assert navire.contient_case(3, 0, 1) is False
    assert navire.contient_case(0, 2, 1) is False
    assert navire.contient_case(1, 1, 0) is False
