from navire import *


class Carte:
    """Représente une carte."""

    def __init__(self):
        """Définition d'une carte."""
        self.navires = []
        self.cases = []
        z = 0
        while z < 3:
            y = 0
            while y < 15:
                x = 0
                while x < 15:
                    self.cases.append(Case(x, y, z))
                    x += 1
                y += 1
            z += 1

    def mise_a_jour_case(self, x, y, z):
        """Vérifie si un bateau est présent à l'endroit de la carte."""
        for index, case in enumerate(self.cases):
            if case.x == x and case.y == y and case.z == z:
                self.cases[index].impact = True
        return self.check_ship(x, y, z)

    def check_ship(self, x, y, z):
        for navire in self.navires:
            case_touche, etat_attaque = navire.test_impact(x, y, z)
            if etat_attaque:
                return True
        return False

    def positionner_navire(self, x, y, z, sens, type_navire, id):
        """Positionnement d'un navire sur la carte."""
        if type_navire == "Porte-container":
            longueur = 5
            largeur = 2
        elif type_navire == "Porte-avion":
            longueur = 5
            largeur = 1
        elif type_navire == "Destroyer":
            longueur = 4
            largeur = 1
        elif type_navire == "Torpilleur":
            longueur = 3
            largeur = 2
        elif type_navire == "Sous-marin nucléaire":
            longueur = 6
            largeur = 1
        elif type_navire == "Sous-marin de combat":
            longueur = 3
            largeur = 2
        elif type_navire == "Sous-marin de reconnaissance":
            longueur = 2
            largeur = 1
        navire = Navire(id, longueur, largeur, type_navire)
        self.navires.append(navire)
        index = self.trouver_navire(id)
        self.navires[index].set_position(x, y, z, sens)

    def trouver_navire(self, id):
        for index, navire in enumerate(self.navires):
            if navire.id == id:
                return index
        return "ERR"
