from carte import Carte, Case, Navire
from reseau import *
from PySide2.QtCore import Slot, QObject, Signal, Property


class Jeu(QObject):
    """Instance de jeu, c'est cette instance qui va s'occuper du déroulement
    de la partie et de la gestion des différents éléments composant
    cette partie"""

    def __init__(self):
        """Définit un jeu."""
        super(Jeu, self).__init__()
        self.carte_perso = Carte(False)
        self.carte_adversaire = Carte(True)
        self.connection = Reseau()
        self.nom_adversaire = ""

    def placer_navire(self, x, y, z, sens, type_navire):
        """Place un navire sur la carte

        Parameters:
            x (int): Abscisse du navire (0 <= x < 15)
            y (int): Ordonnée du navire (0 <= y < 15)
            z (int): Profondeur du navire (0 <= z < 3)
            sens (str): Sens du navire (Vertical ou horizontal)
            type_navire (str): Type du navire
        """

        self.carte_perso.positionner_navire(
            x, y, z, sens, type_navire, len(self.carte_perso.navires)
        )

    @Signal
    def navire_place(self):
        """a appeler quand un navire est placé"""
        pass

    @Slot(int, int, int, int, int)
    def ajouter_navire(self, index_case, profondeur, long, larg, rot):
        sens = ""
        type_navire = ""
        print(f"{index_case}-{profondeur}")
        if rot == 90:
            sens = "Vertical"
        else:
            sens = "Horizontal"

        if long == 5 and larg == 2:
            type_navire = "porte-container"

        elif long == 5 and larg == 1:
            type_navire = "Porte-avion"

        elif long == 4 and larg == 1:
            type_navire = "Destroyer"

        elif long == 3 and larg == 2:
            type_navire = "Torpilleur"

        elif long == 6 and larg == 1:
            type_navire = "Sous-marin nucléaire"

        elif long == 3 and larg == 1:
            type_navire = "Sous-marin de combat"

        elif long == 2 and larg == 1:
            type_navire = "Sous-marin de reconnaissance"
        else:
            type_navire = "Erreur"

        if type_navire != "Erreur":
            self.placer_navire(
                index_case % 15,
                index_case // 15,
                profondeur,
                sens,
                type_navire,
            )
            self.navire_place.emit()

    # QML Link part

    # Défense :
    @Signal
    def tir_subit(self):
        """A appeller dès que la carte de défense est modifiée"""
        pass

    @Slot(int, int, result=bool)
    def get_navire_at(self, case_index, depth):
        """return true si un bateau est présent"""
        x = case_index % 15
        y = case_index // 15
        for navire in self.carte_perso.navires:
            for case in navire.cases:
                if x == case.x and y == case.y and depth == case.z:
                    return True
        return False

    @Slot(int, int, result=bool)
    def get_defense_touche(self, case_index, depth):
        """Return true si cette case à subit un tir (idépendant de bateau)"""
        x = case_index % 15
        y = case_index // 15
        for case in self.carte_perso.cases:
            if x == case.x and y == case.y and depth == case.z:
                return case.impact

    # Attaque :
    @Signal
    def tir_feedback_received(self):
        """A appeller dès que notre carte d'attaque est mise à jour"""
        pass

    @Slot(int, result="QVariantList")
    def get_case_attaque(self, index):
        """Return une liste de taille 3, indiquant à quels niveaux
                                            des bateaux ont été touchés"""
        liste_touche = []
        niveau = 0
        while niveau < 3:
            # TODO && bateau présent
            case = self.carte_adversaire.cases[niveau * 225 + index]
            liste_touche.append(case.impact)
            niveau += 1
        return liste_touche

    @Slot(int, result=bool)
    def get_case_manque(self, index):
        """return true si on a tire sur la case mais que rien n'a été touché"""
        navire = False
        niveau = 0
        while niveau < 3:
            navire |= self.carte_adversaire.cases[
                niveau * 225 + index
            ].presence_bateau
            niveau += 1
        return sum(get_case_attaque(index)) == 3

    @Slot()
    def simulate(self):
        self.recevoir_tir(1, 2)

    def recevoir_tir(self, x, y):
        """Gère les opérations liées à la réception d'un tir :
            - Mise à jour de l'état de la case
            - Analyse du résulat du tir (touché ou non) et de l'étage concerné

            Parameters:
                x (int): Abscisse du tir (0 <= x < 15)
                y (int): Ordonnée du tir (0 <= y < 15)

            Returns:
                (bool, int): Tuple contenant l'état du tir et l'étage concerné
        """

        etage = 0
        etat_tir = False
        while not etat_tir and etage < 3:
            etat_tir = self.carte_perso.mise_a_jour_case(x, y, etage)
            etage += 1
        self.tir_subit.emit()
        return (etat_tir, etage - 1)

    def parse_message(self, trame):
        """ Découpe la trame en fonction de son type:
            - Connexion(ID=1) : Trame de connexion envoyée par le client.
            Renvoie :
                - Longueur du nom d'un joueur
                - Nom du joueur
            - Lancé de missile(ID=2) : Trame d'envoi de tir. Renvoie :
                - Abscisse (entre 1 et 15)
                - Ordonnée (entre 1 et 15)
            - Réponse au lancé(ID=3) : Trame de réponse à un tir adverse.
            Renvoie :
                - Résultat du tir :
                    - 0: Raté
                    - 1: bateau touché
                    - 2: sous-marin de surface touché
                    - 3: sous-marin profond touché
                - Etat bateau :
                    - 0: non-coulé
                    - 1: coulé

        """

        if trame[0] == 1:
            longueur_nom = trame[1]
            index = 2
            while index < longueur_nom:
                self.nom_adversaire += chr(trame[index])
        elif trame[0] == 2:
            # Reception d'un tir
            x = trame[1]
            y = trame[2]
            return (x, y)
        elif trame[0] == 3:
            # Récupération du résultat d'un tir
            if trame[1] == 0:  # Raté
                resultat_tir = "Rate"
            elif trame[1] == 1:  # Touché bateau
                resultat_tir = "Touche_bateau"
            elif trame[1] == 2:  # Touché sous-marin de surface
                resultat_tir = "Touche_sous_marin_surface"
            elif trame[1] == 3:  # Touché sous-marin profond
                resultat_tir = "Touche_sous_marin_profond"

            if trame[2] == 0:
                etat_bateau = "Coule"
            elif trame[2] == 1:
                etat_bateau = "Non_coule"

            return (resultat_tir, etat_bateau)

        else:
            return (None, None)

    def tirer(self, x, y):
        """ Envoi d'un tir à l"adversaire et récupération du résultat de ce
        tir, ainsi que l'état de l'éventuel bateau touché (coulé ou non coulé)

        Parameters:
            x(int): abscisse du tir (1 <= x <= 15)
            y(int): ordonnée du tir (1 <= y <= 15)

        Returns:
            (int, bool): Tuple contenant le résultat du tir envoyé ainsi que
                         l'état de l'éventuel bateau concerné.
        """
        self.a_tire = True
        message = bytearray([2, x, y])
        self.connection.envoyer_trame(message)
        reponse_tir = self.connection.recevoir_trame(3)
        resultat_tir, etat_bateau = self.parse_message(reponse_tir)
        if resultat_tir:
            self.carte_adversaire.mise_a_jour_case(x, y, resultat_tir - 1)
        else:
            # Pas de bateau touché, impact sur les trois couches
            self.carte_adversaire.mise_a_jour_case(x, y, 0)
            self.carte_adversaire.mise_a_jour_case(x, y, 1)
            self.carte_adversaire.mise_a_jour_case(x, y, 2)

    def partie(self):
        while not self.is_fin_partie():
            tour = 0
            while tour < 2:
                if (tour == 0 and self.reseau.isclient) or (
                    tour == 1 and not self.reseau.isclient
                ):
                    while not self.a_tire:
                        pass
                    self.a_tire = False
                elif (tour == 0 and not self.reseau.isclient) or (
                    tour == 1 and self.reseau.isclient
                ):
                    message_tir = self.reseau.recevoir_trame(3)
                    x, y = self.parse_message(message_tir)
                    self.recevoir_tir(x, y)
                tour += 1

    # Partie réseau, passage d'appel de fonction

    @Slot(str, str)
    def seConnecter(seft, ip, port):
        self.connection.se_connecter(ip, port)
        self.partie()

    @Slot(result=str)
    def getIP(self):
        return self.connection.get_ip()

    @Slot(result=str)
    def getPort(self):
        return self.connection.port

    @Slot()
    def heberger(self):
        self.connection.heberger()
        self.partie()
