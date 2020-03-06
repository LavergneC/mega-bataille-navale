from navire import *


class Carte:
    """ Représente une carte. Elle peut être de deux types différents
    (defense ou attaque). Son type jouera sur le type des cases contenue. """

    def __init__(self, is_carte_attaque):
        """Définition d'une carte."""
        self.navires = []
        self.cases = []
        self.is_carte_attaque = is_carte_attaque
        z = 0
        while z < 3:
            y = 0
            while y < 15:
                x = 0
                while x < 15:
                    if self.is_carte_attaque:
                        self.cases.append(CaseAttaque(x, y, z))
                    else:
                        self.cases.append(Case(x, y, z))
                    x += 1
                y += 1
            z += 1

    def mise_a_jour_case(self, x, y, z):
        """Met à jour la case concernée par le tir et renvoie le résultat de
        l'attaque

        Parameters:
            x(int): Abscisse de la case (0 <= x < 15)
            y(int): Ordonnée de la case (0 <= y < 15)
            z(int): Profondeur de la case (0 <= z < 3)

        Returns :
            etat_attaque(bool): Etat de l'attaque subie"""
        for index, case in enumerate(self.cases):
            if case.x == x and case.y == y and case.z == z:
                self.cases[index].impact = True
        return self.check_ship(x, y, z)

    def mise_a_jour_carte_attaque(self, x, y, resultat_tir):
        """ Met à jour la case de la carte adverse après y avoir effectué un tir

        Parameters:
            x(int): Abscisse de la case(0 <= x <= 15)
            y(int): Ordonnée le case (0 <= y <= 15)
            resultat_tir(int): Resultat de notre tir :
                0 - Non touché
                1 - Bateau touché
                2 - Sous marin de surface touché
                3 - Sous marin profond
        """
        profondeur = 0
        is_touche = False
        while profondeur < 3 and not is_touche:
            for index, case in enumerate(self.cases):
                if case.x == x and case.y == y and case.z == profondeur:
                    if profondeur == resultat_tir - 1:
                        self.cases[index].presence_bateau = True
                        is_touche = True
                    self.cases[index].impact = True
                    break
            profondeur += 1

    def check_ship(self, x, y, z):
        """Test si l'un des navires est touché par les coordonnées de l'attaque
        passée en paramètre et si c'est le cas, met à jour l'état de la case du
        bateau concerné

        Parameters :
            x(int) : abscisse de l'attaque subie (0 <= x < 15)
            y(int): ordonnées de l'attaque subie (0 <= y < 15)
            z(int): profondeur de l'attaque subie (0 <= z < 3)

        Returns:
            bool: Retourne si l'attaque subie a touché l'un de nos bateaux

        """
        for index, navire in enumerate(self.navires):
            case_touche, etat_attaque = self.navires[index].test_impact(
                x, y, z
            )
            if etat_attaque:
                return (True, self.navires[index].test_bateau_detruit())
        return (False, False)

    def positionner_navire(self, x, y, z, sens, type_navire, id):
        """Créé un bateau et initialise sa taille et sa position dans la carte.
        IL faut savoir que les coordonnées passées en paramètre concernent la
        première case du bateau qui est la case la plus haute et la plus à
        gauche du bateau.

        Parameters:
            x (int): abscisse de la première case du navire
            y (int): ordonnée de la première case du navire
            z (int): profondeur du navire
            sens (str): sens du navire (Vertical ou Horizontal)
            type_navire (str): type du navire

        """

        if type_navire == "porte-container":
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
            largeur = 1
        elif type_navire == "Sous-marin de reconnaissance":
            longueur = 2
            largeur = 1

        navire = Navire(id, longueur, largeur, type_navire)
        self.navires.append(navire)
        index = self.trouver_navire(id)
        self.navires[index].set_position(x, y, z, sens)

    def trouver_navire(self, id):
        """ Retoune l'index du bateau correspondant à l'identifiant passé en
        paramètre.

        Parameters:
            id (int): Identifant du bateau

        Returns:
            index(int): Index du navire dans la liste des navires contenus
            dans la carte.

        """
        for index, navire in enumerate(self.navires):
            if navire.id == id:
                return index
        return "ERR"
