from carte import Carte, Case, Navire
from reseau import *
import threading
import time
from PySide2.QtCore import Slot, QObject, Signal, Property


class Jeu(QObject):
    """Instance de jeu, c'est cette instance qui va s'occuper du déroulement
    de la partie et de la gestion des différents éléments composant
    cette partie"""

    def __init__(self):
        """Définit un jeu."""
        super().__init__()
        self.carte_perso = Carte(False)
        self.carte_adversaire = Carte(True)
        self.nom_joueur = "Capichef"
        self.partie_perdue = False
        self.partie_gagnee = False
        self.compteur_bateau_coule = 0
        self.nom_adversaire = ""
        self.droit_de_tir = False

    def init_reseau(self):
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
            x, y, z, sens, type_navire, len(self.carte_perso.navires)
        )

    @Signal
    def navire_place(self):
        """a appeler quand un navire est placé"""

    @Signal
    def connection_effectuee(self):
        pass

    @Slot(str)
    def set_nom(self, new_nom):
        print(new_nom)
        self.nom_joueur = new_nom

    @Slot(int, int, int, int, int, result=bool)
    def position_navire_disponible(
        self, index_case, profondeur, long, larg, rot
    ):
        """ Return si il est possible de placer un bateau à l'endroit ciblé

        Parameters:
            index_case (int): Numéro de la case (0 <= index_case < 225)
            profoncdeur (int): Niveau du bateau (0 <= profondeur < 4)
            long (int): Longeur du bateau à poser (2 <= long <= 6)
            larg (int): Hauteur du bateau à poser (1 ou 2)
            rot (int): Rotation du bateau (0 ou 90)
        """
        sens = ""
        type_navire = ""

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
            return False

        if sens == "Vertical":
            taille_x = larg
            taille_y = long
        else:
            taille_x = long
            taille_y = larg

        if (not ("marin" in type_navire)) and (
            profondeur == 1 or profondeur == 2
        ):
            return False

        x = index_case % 15
        y = index_case // 15
        cpt_x = 0
        while cpt_x < taille_x:
            cpt_y = 0
            while cpt_y < taille_y:
                for navire in self.carte_perso.navires:
                    if navire.contient_case(x + cpt_x, y + cpt_y, profondeur):
                        return False
                if x + cpt_x >= 15 or y + cpt_y >= 15:
                    return False
                cpt_y += 1
            cpt_x += 1
        return True

    @Slot(int, int, int, int, int, result=bool)
    def ajouter_navire(self, index_case, profondeur, long, larg, rot):
        sens = ""
        type_navire = ""
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

    @Slot(int, result="QVariantList")
    def get_case_attaque(self, index):
        """Return une liste de taille 3, indiquant à quels niveaux
                                            des bateaux ont été touchés"""
        liste_touche = []
        niveau = 0
        while niveau < 3:
            case = self.carte_adversaire.cases[niveau * 225 + index]
            liste_touche.append(case.impact and case.presence_bateau)
            if index == 0:
                print(case.impact, case.presence_bateau)
            niveau += 1
        return liste_touche

    @Slot(int, result=bool)
    def get_case_manque(self, index):
        """return true si on a tire sur la case mais que rien n'a été touché"""
        return (
            sum(self.get_case_attaque(index)) == 0
            and self.carte_adversaire.cases[2 * 225 + index].impact
        )

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
            etat_tir, etat_navire = self.carte_perso.mise_a_jour_case(
                x, y, etage
            )
            etage += 1
        self.tir_subit.emit()
        return (etat_tir, etage, etat_navire)

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
            print(longueur_nom)
            index = 0
            nom_adv = ""
            while index < longueur_nom:
                nom_adv += chr(trame[index + 2])
                index += 1
            print(nom_adv)
            return nom_adv
        elif trame[0] == 2:
            # Reception d'un tir
            x = trame[1]
            y = trame[2]
            return (x, y)
        elif trame[0] == 3:
            # Récupération du résultat d'un tir
            resultat_tir = trame[1]
            if trame[2] == 0:
                etat_bateau = "Non_coule"
            elif trame[2] == 1:
                etat_bateau = "Coule"

            return (resultat_tir, etat_bateau)

        else:
            return (None, None)

    @Slot(int, int)
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
        message = bytearray([2, x, y])
        self.connection.envoyer_trame(message)
        reponse_tir = self.connection.recevoir_trame(3)
        print(f'Jeu::tirer Reçu : {reponse_tir}')
        resultat_tir, etat_bateau = self.parse_message(reponse_tir)
        print(f'Jeu::tirer Parsé : result{reponse_tir}, etat{etat_bateau}')
        if etat_bateau == "Coule":
            self.compteur_bateau_coule += 1
        self.carte_adversaire.mise_a_jour_carte_attaque(x, y, resultat_tir)
        self.droit_de_tir = False

        return (resultat_tir, etat_bateau)

    @Slot(result=bool)
    def droit_de_tirer(self):
        return self.droit_de_tir

    def partie(self):
        if self.connection.isclient:
            self.thread_seConnecter.join()
        else:
            self.thread_heberger.join()
        print("Connection OK")
        while not self.fin_partie():
            tour = 0
            while tour < 2:
                if (tour == 0 and self.connection.isclient) or (
                    tour == 1 and not self.connection.isclient
                ):
                    self.droit_de_tir = True
                    print("Attente tire...")
                    while self.droit_de_tir:
                        time.sleep(0.1)
                    print("Tire OK")
                elif (tour == 0 and not self.connection.isclient) or (
                    tour == 1 and self.connection.isclient
                ):
                    print("Attente tir adv...")
                    message_tir = self.connection.recevoir_trame(3)
                    print("Tir adv OK...")
                    x, y = self.parse_message(message_tir)
                    etat_tir, etage, etat_navire = self.recevoir_tir(x, y)

                    if etat_tir:
                        message = bytearray([3, etage, etat_navire])
                    else:
                        message = bytearray([3, 0, 0])
                    self.connection.envoyer_trame(message)
                    print(f"Envoyer : {message}")
                    print("retour tir Adv OK")

                tour += 1
        self.partie_en_cours_changed.emit()

    @Signal
    def partie_en_cours_changed(self):
        pass

    # Partie réseau, passage d'appel de fonction

    @Slot(str, int)
    def seConnecter(self, ip, port):
        self.thread_seConnecter = threading.Thread(
            target=self.seConnecter_thread, args=[ip, port]
        )
        self.thread_partie = threading.Thread(target=self.partie)
        self.thread_seConnecter.start()
        self.thread_partie.start()

    def seConnecter_thread(self, ip, port):
        self.connection.se_connecter(ip, port)
        self.connection_effectuee.emit()
        liste_car = list(map(ord, self.nom_joueur))
        message = bytearray([1, len(self.nom_joueur), *liste_car])
        print(f"Message se co : {message}")
        self.connection.envoyer_trame(message)
        message = self.connection.recevoir_trame(1024)
        self.nom_adversaire = self.parse_message(message)

    @Slot(result=str)
    def getIP(self):
        return self.connection.get_ip()

    @Slot(result=int)
    def getPort(self):
        return self.connection.port

    @Slot()
    def heberger(self):
        self.thread_heberger = threading.Thread(target=self.heberger_thread)
        self.thread_partie = threading.Thread(target=self.partie)
        print("Start heberger & partie")
        self.thread_heberger.start()
        self.thread_partie.start()

    def heberger_thread(self):
        self.connection.heberger()
        print("CONNECTION OK")
        self.connection_effectuee.emit()
        message = self.connection.recevoir_trame(1024)
        print("Message reçue")
        self.nom_adversaire = self.parse_message(message)
        print(f"Nom adv : {self.nom_adversaire}")
        liste_car = list(map(ord, self.nom_joueur))
        message = bytearray([1, len(self.nom_joueur), *liste_car])
        self.connection.envoyer_trame(message)

    def fin_partie(self):
        """Cette méthode sert à savoir quand la partie est finie et si
        c'est nous qui avons perdu ou l'adversaire
        """
        for navire in self.carte_perso.navires:
            if navire.isdetruit is False:
                self.partie_perdue = False
                break
        else:
            self.partie_perdue = True

        if self.compteur_bateau_coule == 18:
            self.partie_gagnee = True
        else:
            self.partie_gagnee = False

    @Slot(result=bool)
    def get_partie_gagnee(self):
        return self.partie_gagnee
