import socket


class Reseau:
    """ Interface réseau permettant d'intéragir avec un client ou de se
        comporter en tant que serveur TCP."""

    def __init__(self):
        """ Initialisation de l'interface en créant et configurant une
            socket TCP et en initialisant le port utilisé à 12800"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 12800
        self.isclient = True

    def get_ip(self):
        """Attribue la valeur de l'adresse IP de l'hôte à l'attribut
           concerné."""
        hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(hostname + ".local")

    def se_connecter(self, ip, port):
        """ (Client) Se connecte à l'hôte auquel appartient l'adresse IP
            passé en paramètre

        Parameters:
            ip (str): Adresse IP de l'hôte auquel on souhaite se connecter
            port (int): Port de l'hôte en écoute sur lequel on va communiquer

        """
        self.isclient = True
        self.socket.connect((ip, port))

    def heberger(self):
        """ (Serveur) Méthode bloquante permettant d'être configuré en tant
            que serveur attendant qu'un client se connecte et crée une
            socket de connexion avec ce client une fois qu'il nous a contacté
        """
        self.isclient = False
        self.infos_connexion = (self.ip_address, self.port)
        self.socket.bind(self.infos_connexion)
        self.socket.listen(2)
        self.socketclient, self.infos_connexion = self.socket.accept()
        print(self.infos_connexion)

    def envoyer_trame(self, message):
        """ Envoi d'un message.

        Parameters:
            message (byte): Message à envoyer

        """

        message = str.encode(message)
        if self.isclient:
            self.socket.send()
        else:
            self.socketclient.send(message)

    def recevoir_trame(self, taille_message):
        """ Méthode bloquante attendant un message et le retourne

        Parameters:
            taille (int): taille du message attendue

        Returns:
            message (str): message reçue
        """

        if self.isclient:
            message = self.socket.recv(taille_message)
        else:
            message = self.socketclient.recv(taille_message)
        return message
