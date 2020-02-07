import sys

sys.path.insert(1, 'src')

from navire import *

def test_test_impact():
    navire = Navire(0, 3, 1, "Calypso")
    navire.cases.append(Case(1, 2, 1))
    navire.cases.append(Case(2, 2, 1))
    navire.cases.append(Case(3, 2, 1))

    assert navire.test_impact(4, 2, 1)[1] == False
    assert navire.test_impact(2, 2, 1)[1] == True

    assert navire.test_impact(1, 1, 1)[1] == False
    assert navire.test_impact(2, 2, 2)[1] == False

    assert navire.test_impact(-2, 2, 1)[1] == False
    assert navire.test_impact(2.2, 2, 1)[1] == False
