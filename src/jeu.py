from carte import Carte, Case, Navire
from PySide2.QtCore import Slot, QObject, Signal, Property


class Jeu(QObject):
    """Represente le jeu."""

    
    def __init__(self):
        super(Jeu, self).__init__()
        self.carte_perso = Carte()
        self.carte_adversaire = Carte()

    def placer_navire(self, x, y, z, sens, name):
        pass

# QML Link part

# Défense :
    # A appeller dès que la carte de défense est modifiée
    @Signal
    def tir_subit(self):
        pass

    # return true si un bateau est présent
    @Slot(int, int, result = bool)
    def get_navire_at(self, case_index, depth):
        return True

    # Return true si cette case à subit un tir (idépendant de bateau)
    @Slot(int, int, result = bool)
    def get_defense_touche(self, case_index, depth):
        return True

# Attaque :
    # A appeller dès que notre carte d'attaque est mise à jour
    @Signal
    def tir_feedback_received(self):
        pass

    # Return une liste de taille 3, indiquant à quels niveaux 
    # des bateaux ont été touchés
    @Slot(int, result = 'QVariantList')
    def get_case_attaque(self, index):
        return [0,1,0]

    # return true si on a tire sur la case mais que rien n'a été touché
    @Slot(int, result = bool)
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
            etat_tir = self.carte_perso.check_ship(x, y, etage)

        self.tir_subit.emit()

        return (etat_tir, etage)

    def parse_message(self, trame):
        """Decoupe les trames reçues."""
        if trame[0] == 2:
            # Reception d'un tir
            x = trame[1]
            y = trame[2]
            return (x, y)
        else:
            return (None, None)
