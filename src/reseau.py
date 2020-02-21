import socket


class Reseau:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 12800
        self.isclient = True

    def get_ip(self):
        hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(hostname)

    def se_connecter(self, ip, port):
        self.isclient = True
        self.socket.connect((ip, port))

    def heberger(self):
        self.isclient = False
        self.infos_connexion = (self.ip_address, self.port)
        self.socket.bind(self.infos_connexion)
        self.socket.listen(2)
        self.socketclient, self.infos_connexion = self.socket.accept()
        print(self.infos_connexion)

    def envoyer_trame(self, message):
        message = str.encode(message)
        if self.isclient:
            self.socket.send()
        else:
            self.socketclient.send(message)

    def recevoir_trame(self, taille_message):
        if self.isclient:
            message = self.socket.recv(taille_message)
        else:
            message = self.socketclient.recv(taille_message)
        return message
