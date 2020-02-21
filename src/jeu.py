from carte import Carte, Case, Navire
from reseau import *
from PySide2.QtCore import Slot, QObject, Signal, Property


class Jeu(QObject):
    """Instance de jeu, c'est cette instance qui va s'occuper du déroulement de la partie et de la gestion des différents éléments composant cette partie"""

    def __init__(self):
        """Définit un jeu."""
        super(Jeu, self).__init__()
        self.carte_perso = Carte()
        self.carte_adversaire = Carte()
        self.connection = Reseau()

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
            x, y, z, "Vertical", type_navire, len(self.carte_perso.navires)
        )

    # QML Link part

    # Défense :
    # A appeller dès que la carte de défense est modifiée
    @Signal
    def tir_subit(self):
        pass

    # return true si un bateau est présent
    @Slot(int, int, result=bool)
    def get_navire_at(self, case_index, depth):
        return True

    # Return true si cette case à subit un tir (idépendant de bateau)
    @Slot(int, int, result=bool)
    def get_defense_touche(self, case_index, depth):
        return True

    # Attaque :
    # A appeller dès que notre carte d'attaque est mise à jour
    @Signal
    def tir_feedback_received(self):
        pass

    # Return une liste de taille 3, indiquant à quels niveaux
    # des bateaux ont été touchés
    @Slot(int, result="QVariantList")
    def get_case_attaque(self, index):
        return [0, 1, 0]

    # return true si on a tire sur la case mais que rien n'a été touché
    @Slot(int, result=bool)
    def get_case_manque(index):
        return True

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
            etage += 1
            etat_tir = self.carte_perso.mise_a_jour_case(x, y, etage)
        self.tir_subit.emit()
        return (etat_tir, etage)

    def parse_message(self, trame):
        """ Découpe la trame en fonction de son type:
            - Connexion(ID=1) : Trame de connexion envoyée par le client. Renvoie :
                - Longueur du nom d'un joueur
                - Nom du joueur
            - Lancé de missile(ID=2) : Trame d'envoi de tir. Renvoie :
                - Abscisse (entre 1 et 15)
                - Ordonnée (entre 1 et 15)
            - Réponse au lancé(ID=3) : Trame de réponse à un tir adverse. Renvoie :
                - Résultat du tir :
                    - 0: Raté
                    - 1: bateau touché
                    - 2: sous-marin de surface touché
                    - 3: sous-marin profond touché
                - Etat bateau :
                    - 0: non-coulé
                    - 1: coulé

        """

        if trame[0] == 2:
            # Reception d'un tir
            x = trame[1]
            y = trame[2]
            return (x, y)
        elif trame[0] == 3:
            # Récupération du résultat d'un tir
            if trame[1] == 0:  #  Raté
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
        """ Envoi d'un tir à l"adversaire et récupération du résultat de ce tir, ainsi que l'état de l'éventuel bateau touché(coulé ou non coulé

        Parameters:
            x(int): abscisse du tir (1 <= x <= 15)
            y(int): ordonnée du tir (1 <= y <= 15)

        Returns:
            (int, bool): Tuple contenant le résultat du tir envoyé ainsi que l'état de l'éventuel bateau concerné.
        """

        message = bytearray([2, x, y])
        self.connection.envoyer_trame(message)
        reponse_tir = self.connection.recevoir_trame(3)
        resultat_tir, etat_bateau = self.parse_message(reponse_tir)

    # Partie réseau, passage d'appel de fonction

    @Slot(str, str)
    def seConnecter(seft, ip, port):
        pass

    @Slot(result=str)
    def getIP(self):
        pass

    @Slot(result=str)
    def getPort(self):
        pass

    @Slot()
    def heberger(self):
        pass
