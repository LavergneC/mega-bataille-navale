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

    def check_ship(self, x, y, z):
        """Vérifie si un bateau est présent à l'endroit de la carte."""
        for navire in self.navires:
            case_touche, etat_attaque = navire.test_impact(x, y, z)
            if etat_attaque:
                for index, case in enumerate(self.cases):
                    if case.index == case_touche.index:
                       self.cases[index].impact = True
                return True
        return False

    def positionner_navire(self, x, y, z, sens, name):
        """Positionnement d'un navire sur la carte."""
        pass
