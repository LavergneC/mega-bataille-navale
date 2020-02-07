import sys

sys.path.insert(1, "src")

from jeu import Jeu
from carte import Carte
from navire import Navire
from case import Case


def test_recevoir_tir():
    """Test de la fonction recevoir un tir."""
    jeu = Jeu()

    navire = Navire(0, 3, 1, "AlainBernard")
    jeu.carte_perso.navires.append(navire)
    jeu.carte_perso.navires[0].cases.append(Case(11, 5, 1))
    jeu.carte_perso.navires[0].cases.append(Case(10, 5, 1))
    jeu.carte_perso.navires[0].cases.append(Case(9, 5, 1))

    navire1 = Navire(1, 4, 1, "HollandaisVolant")
    jeu.carte_perso.navires.append(navire1)
    jeu.carte_perso.navires[1].cases.append(Case(1, 7, 2))
    jeu.carte_perso.navires[1].cases.append(Case(2, 7, 2))
    jeu.carte_perso.navires[1].cases.append(Case(3, 7, 2))
    jeu.carte_perso.navires[1].cases.append(Case(4, 7, 2))

    assert jeu.recevoir_tir(0, 0)[0] == False
    assert jeu.recevoir_tir(4, 5)[0] == False
    assert jeu.recevoir_tir(11, 5) == (True, 1)
    assert jeu.recevoir_tir(4, 7) == (True, 2)


def test_parse_message():
    """Test de la fonction parse_message."""
    jeu = Jeu()

    trame = []
    trame.append(2)
    trame.append(1)
    trame.append(5)
    assert jeu.parse_message(trame) == (1, 5)

    #  Bad Message ID
    trame1 = []
    trame1.append(0)
    trame1.append(1)
    trame1.append(1)
    assert jeu.parse_message(trame1) == (None, None)

    trame2 = []
    trame2.append(2)
    trame2.append(0)
    trame2.append(5)
    assert jeu.parse_message(trame2) == (0, 5)

    trame3 = []
    trame3.append(2)
    trame3.append(5)
    trame3.append(17)
    assert jeu.parse_message(trame3) == (5, 17)

    trame4 = []
    trame4.append(2)
    trame4.append(18)
    trame4.append(0)
    assert jeu.parse_message(trame4) == (18, 0)

    #  Negative message ID
    trame5 = []
    trame5.append(-5)
    trame5.append(18)
    trame5.append(0)
    assert jeu.parse_message(trame5) == (None, None)

    trame6 = []
    trame6.append(2)
    trame6.append(-5)
    trame6.append(15)
    assert jeu.parse_message(trame6) == (-5, 15)

    trame8 = []
    trame8.append(2.0)
    trame8.append(2.5)
    trame8.append(5.5)
    assert jeu.parse_message(trame8) == (2.5, 5.5)
