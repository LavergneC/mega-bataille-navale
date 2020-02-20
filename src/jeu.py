from carte import Carte, Case, Navire
from reseau import *
from PySide2.QtCore import Slot, QObject, Signal, Property


class Jeu(QObject):
    """Represente le jeu."""

    def __init__(self):
        """Défini un jeu."""
        super(Jeu, self).__init__()
        self.carte_perso = Carte()
        self.carte_adversaire = Carte()
        self.connection = Reseau()

    def placer_navire(self, x, y, z, sens, type_navire):
        """Place un bateau sur jeu."""
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
        """Gere la reception d'un tir."""
        etage = 0
        etat_tir = False
        while not etat_tir and etage < 3:
            etage += 1
            etat_tir = self.carte_perso.mise_a_jour_case(x, y, etage)
        self.tir_subit.emit()
        return (etat_tir, etage)

    def parse_message(self, trame):
        """Découpe les trames reçues."""
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
