from case import *


class Navire:
    """Représente un navire."""

    def __init__(self, id, longueur, largeur, nom):
        """Défini un navire."""
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
        """Permet de définir les coordonnées d'un bateau."""
        cpt_longueur = 0
        if sens == "Vertical":
            max_longueur = self.largeur
            max_largeur = self.longueur
        elif sens == "Horizontal":
            max_longueur = self.longueur
            max_largeur = self.largeur
        while cpt_longueur < max_longueur:
            cpt_largeur = 0
            while cpt_largeur < max_largeur:
                self.cases.append(Case(x + cpt_longueur, y + cpt_largeur, z))
                cpt_largeur += 1
            cpt_longueur += 1
