import sys
import pytest

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

    assert jeu.recevoir_tir(0, 0)[0] is False
    assert jeu.recevoir_tir(4, 5)[0] is False
    assert jeu.recevoir_tir(11, 5) == (True, 1)
    assert jeu.recevoir_tir(4, 7) == (True, 2)


liste_parametres = []
liste_parametres.append(([2, 1, 5], (1, 5)))
liste_parametres.append(([0, 1, 1], (None, None)))
liste_parametres.append(([2, 0, 5], (0, 5)))
liste_parametres.append(([2, 5, 17], (5, 17)))
liste_parametres.append(([2, 18, 0], (18, 0)))
liste_parametres.append(([-5, 18, 0], (None, None)))
liste_parametres.append(([2, -5, 15], (-5, 15)))
liste_parametres.append(([2.0, 2.5, 5.5], (2.5, 5.5)))

liste_parametres.append(([3, 0, 1], ("Rate", "Non_coule")))
liste_parametres.append(([3, 1, 1], ("Touche_bateau", "Non_coule")))
liste_parametres.append(
    ([3, 2, 1], ("Touche_sous_marin_surface", "Non_coule"))
)
liste_parametres.append(([3, 3, 0], ("Touche_sous_marin_profond", "Coule")))


@pytest.mark.parametrize("test_input,expected", liste_parametres)
def test_parse_message(test_input, expected):
    """Test de la fonction parse_message."""
    jeu = Jeu()
    assert jeu.parse_message(test_input) == expected


def test_placer_navire():
    jeu = Jeu()

    jeu.placer_navire(5, 5, 1, "Vertical", "Destroyer")
    assert jeu.carte_perso.navires[0].cases[0].x == 5
    assert jeu.carte_perso.navires[0].cases[0].y == 5
    assert jeu.carte_perso.navires[0].cases[0].z == 1

    assert jeu.carte_perso.navires[0].cases[1].x == 5
    assert jeu.carte_perso.navires[0].cases[1].y == 6
    assert jeu.carte_perso.navires[0].cases[1].z == 1

    assert jeu.carte_perso.navires[0].cases[2].x == 5
    assert jeu.carte_perso.navires[0].cases[2].y == 7
    assert jeu.carte_perso.navires[0].cases[2].z == 1

    assert not jeu.carte_perso.navires[0].cases[2].x == 6
    assert not jeu.carte_perso.navires[0].cases[2].y == 8
    assert not jeu.carte_perso.navires[0].cases[1].z == 2

    jeu.placer_navire(0, 0, 1, "Horizontal", "Sous-marin nucléaire")
    assert jeu.carte_perso.navires[1].cases[1].x == 1
    assert jeu.carte_perso.navires[1].cases[1].y == 0
    assert jeu.carte_perso.navires[1].cases[1].z == 1


def test_get_navire_at():
    jeu = Jeu()

    jeu.placer_navire(2, 2, 2, "Horizontal", "Sous-marin de combat")
    assert jeu.get_navire_at(32, 2) is True
    assert jeu.get_navire_at(33, 2) is True

    assert jeu.get_navire_at(32, 1) is False
    assert jeu.get_navire_at(33, 0) is False

    assert jeu.get_navire_at(31, 2) is False
    assert jeu.get_navire_at(34, 2) is True


def test_defense_touche():
    jeu = Jeu()

    jeu.placer_navire(1, 2, 1, "Horizontal", "Sous-marin de reconnaissance")
    jeu.recevoir_tir(0, 0)
    jeu.recevoir_tir(1, 2)
    jeu.recevoir_tir(3, 3)

    assert jeu.get_defense_touche(0, 2) is True
    assert jeu.get_defense_touche(0, 1) is True
    assert jeu.get_defense_touche(0, 0) is True

    assert jeu.get_defense_touche(31, 2) is False
    assert jeu.get_defense_touche(31, 1) is True
    assert jeu.get_defense_touche(31, 0) is True

    assert jeu.get_defense_touche(32, 2) is False
    assert jeu.get_defense_touche(32, 1) is False
    assert jeu.get_defense_touche(32, 0) is False


def test_ajouter_navire():
    jeu = Jeu()

    jeu.ajouter_navire(0, 0, 5, 2, 0)
    jeu.ajouter_navire(60, 0, 5, 1, 0)
    jeu.ajouter_navire(66, 0, 4, 1, 90)
    jeu.ajouter_navire(10, 0, 3, 2, 0)
    jeu.ajouter_navire(0, 1, 6, 1, 0)
    jeu.ajouter_navire(30, 1, 3, 1, 90)
    jeu.ajouter_navire(105, 2, 2, 1, 90)
    jeu.ajouter_navire(105, 1, 5, 3, 90)

    assert jeu.get_navire_at(0, 0) is True
    assert jeu.get_navire_at(3, 0) is True
    assert jeu.get_navire_at(5, 0) is False

    assert jeu.get_navire_at(60, 0) is True
    assert jeu.get_navire_at(0, 2) is False
    assert jeu.get_navire_at(75, 0) is False

    assert jeu.get_navire_at(66, 2) is False
    assert jeu.get_navire_at(66, 0) is True
    assert jeu.get_navire_at(67, 0) is False

    assert jeu.get_navire_at(225, 0) is False
    assert jeu.get_navire_at(125, 1) is False
    assert jeu.get_navire_at(13, 0) is False

    assert jeu.get_navire_at(0, 1) is True
    assert jeu.get_navire_at(33, 0) is False
    assert jeu.get_navire_at(6, 1) is False

    assert jeu.get_navire_at(30, 2) is False
    assert jeu.get_navire_at(45, 1) is True
    assert jeu.get_navire_at(31, 1) is False

    assert jeu.get_navire_at(105, 2) is True
    assert jeu.get_navire_at(115, 0) is False
    assert jeu.get_navire_at(106, 2) is False

    assert jeu.get_navire_at(105, 1) is False


def test_position_navire_disponible():
    jeu = Jeu()

    jeu.placer_navire(0, 1, 1, "Horizontal", "Sous-marin de combat")

    assert jeu.position_navire_disponible(0, 0, 3, 1, 0) is True
    assert jeu.position_navire_disponible(0, 0, 5, 2, 0) is True
    assert jeu.position_navire_disponible(0, 0, 5, 1, 0) is True
    assert jeu.position_navire_disponible(0, 0, 4, 1, 0) is True

    assert jeu.position_navire_disponible(13, 0, 3, 2, 0) is False
    assert jeu.position_navire_disponible(15 * 10, 0, 6, 1, 90) is False
    assert jeu.position_navire_disponible(2 * 15, 2, 3, 4, 0) is False
    assert jeu.position_navire_disponible(1, 1, 2, 1, 90) is False
