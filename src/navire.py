from case import *
from caseattaque import CaseAttaque


class Navire:
    """Représente un navire de n'importe quel type"""

    def __init__(self, id, longueur, largeur, nom):
        """Constructeur d'un navire

        Parameters:
            id(int)
            longueur(int)
            largeur(int)
            nom(str)
        """

        self.longueur = longueur
        self.largeur = largeur
        self.nom = nom
        self.id = id
        self.cases = []
        self.isdetruit = False

    def test_bateau_detruit(self):
        """Teste si le navire est detruit en parcourant les cases.

        Returns :
            True si bateau est detruit False si le bateau est pas detruit.
        """

        for case in self.cases:
            if case.impact is False:
                return False
        return True

    def test_impact(self, x, y, z):
        """Teste si le navire est concerné par un tir adverse aux coordonnées
        passées en paramètre et met à jour l'état de la case
        touchée en cas d'impact.

        Parameters :
            x: abscisse du tir (0 <= x < 15)
            y: ordonnée du tir (0 <= y < 15)
            z: profondeur du tir (0 <= z < 3)

        Returns :
            (case(Case),impact(bool)) : Retourne un tuple contenant la case
            touchée (ou None si le navire n'est pas touché) ainsi que si
            le navire a été touché.
            """
        for index, case in enumerate(self.cases):
            if case.x == x and case.y == y and case.z == z:
                self.cases[index].impact = True
                return (case, True)
            self.isdetruit = self.test_bateau_detruit()
        return (None, False)

    def set_position(self, x, y, z, sens):
        """Initie la position du bateau, il faut savoir que les coordonnées
        passées en paramètre correpondent au point le plus haut ou le
        plus à gauche du bateau.

        Parameters :
            x (int): abscisse de la première case du bateau
            y (int): ordonnée de la première case du bateau

            """

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

    def contient_case(self, x, y, z):
        """ Teste si les coordonnées passées en paramètre sont couverts par une
            case d'un bateau.

        Parameters:
            x (int): abscisse de la case testée (0 <= x  15)
            y (int): ordonnée de case testée (0 <= y < 15)
            z (int): profondeur de la case testée (0 <= z < 3)

        Returns:
            bool: True si la case appartient au navire sinon False
        """

        for case in self.cases:
            if case.x == x and case.y == y and case.z == z:
                return True
        return False
