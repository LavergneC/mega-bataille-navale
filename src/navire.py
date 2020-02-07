from case import *


class Navire:
    """Représente un navire."""

    def __init__(self, id, longueur, largeur, nom):
        self.longueur = longueur
        self.largeur = largeur
        self.nom = nom
        self.id = id
        self.cases = []

    def test_impact(self, x, y, z):
        """Teste si touché."""
        for index, case in enumerate(self.cases):
            if case.x == x and case.y == y and case.z == z:
                self.cases[index].impact = True
                return (case, True)
        return (None, False)

    def set_position(self, x, y, z, sens):
        pass
