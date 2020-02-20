from carte import Carte, Case, Navire
from PySide2.QtCore import Slot, QObject, Signal, Property


class Jeu(QObject):
    """Represente le jeu."""

    def __init__(self):
        """Défini un jeu."""
        super(Jeu, self).__init__()
        self.carte_perso = Carte()
        self.carte_adversaire = Carte()

    def placer_navire(self, x, y, z, sens, type_navire):
        """Place un bateau sur jeu."""
        self.carte_perso.positionner_navire(
            x, y, z, sens, type_navire, len(self.carte_perso.navires)
        )

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
        """Return une liste de taille 3, indiquant à quels niveaux  des bateaux ont été touchés"""
        liste_touche = []
        niveau = 0
        while niveau < 3:
            #TODO && bateau présent
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
            navire &= self.cartek
            niveau += 1

        return sum(get_case_attaque(index)) == 3

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
        else:
            return (None, None)

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
