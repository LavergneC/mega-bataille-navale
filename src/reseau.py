import socket


class Reseau:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 12800

    def get_ip(self):
        hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(hostname)

    def se_connecter(self, ip, port):
        self.socket.connect((ip, port))

    def heberger(self):
        self.infos_connexion = (self.ip_address, self.port)
        self.socket.bind(self.infos_connexion)
        self.socket.listen(2)
        self.socketclient, self.infos_connexion = self.socket.accept()
        print(self.infos_connexion)

    def communication_cote_serveur(self):
        self.socketclient.send(b"Je viens d'accepter  la connexion")

    def communication_cote_client(self):
        message_recu = self.socket.recv(1024)
        print(message_recu)
