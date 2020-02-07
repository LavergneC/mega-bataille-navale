import sys

sys.path.insert(1, 'src')

from carte import *

def test_check_ship():
    carte = Carte()
    navire = Navire(0, 3, 1, "Calypso")
    navire.cases.append(Case(1, 2, 1))
    navire.cases.append(Case(2, 2, 1))
    navire.cases.append(Case(3, 2, 1))
    carte.navires.append(navire)

    assert carte.check_ship(2, 2, 1) == True
    assert carte.check_ship(2, 2, 2) == False
    assert carte.check_ship(2, 3, 1) == False
    assert carte.check_ship(4, 2, 1) == False
