# coding:utf-8
import socket
import protocolClientServer as _pcs

host, port = ('89.168.57.22', 49352)
# host, port = ('localhost', 5566)

class Client:
    def __init__(self):
        print("Lancement de la connexion au serveur...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Créer le socket

        try:
            self.socket.connect((host, port))  # Connecter le socket
            print("Client connecté !")
        except Exception as e:
            print(f"Connexion au serveur échouée ! Erreur: {e}")
            self.socket.close()  # Fermer le socket en cas d'échec de connexion

    def send_order(self, order_code):
        if order_code in _pcs.codes:
            data = _pcs.codes[order_code].encode('utf8')
            self.socket.send(data)  # Utiliser send au lieu de sendto
            print(f"Data sent: {order_code}")

    def start(self):
        self.send_order("PlayerConnect")

    def execute_order(self, order_code):
        if order_code == _pcs.codes["Ping"]:
            print("Ping reçu")
            self.send_order("Pong")

    def communicate_with_server(self):
        self.start()

        while True:
            try:
                data = self.socket.recv(1024).decode('utf8')  # Recevoir des données du serveur
                if data:
                    print(f"Données reçues: {data}")
                    self.execute_order(data)  # Traiter les données reçues
            except Exception as e:
                print(f"Erreur: {e}")
                self.socket.close()  # Fermer le socket en cas d'erreur
                break  # Sortir de la boucle si une erreur se produit

#----------------------------------------------------------------
client = Client()
client.communicate_with_server()
