import socket

class Reseau:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = "12800"

    def get_ip(self):
        hostname = self.socket.gethostname()
        self.ip_address = self.socket.gethostbyname(hostname)

    def se_connecter(self, ip, port):
        self.socket.connect(host=self.ip_address, port=port, timeout=1000)

    def heberger(self):
        self.infos_connexion = (self.ip_address, self.port)
        self.socket.bind(self.infos_connexion)
        socketclient, self.infos_connexion = self.socket.accept()
        print(self.infos_connexion)