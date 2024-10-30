# coding:utf-8
import socket
import protocolClientServer as _pcs
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

host, port = ('89.168.57.22', 49352)
# host, port = ('localhost', 5566)

@dataclass
class DataBase:
    PlayerPosition: Tuple[float, float] = field(default_factory=tuple)  # Format :(x, y)

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

    def send_order(self, order_code, data_content=None):
        if order_code in _pcs.codes:
            # si aucune donnée n'est donnée, considerer qu'il n'y en a pas a donner
            if not data_content:
                data = _pcs.codes[order_code].encode('utf8')
                self.socket.send(data)  # Utiliser send au lieu de sendto
                print(f"Data sent: {order_code}")
            else:
                if order_code == "PositionPlayer":
                    # Vérification si data_content est un tuple de deux floats
                    if isinstance(data_content, tuple) and len(data_content) == 2:
                        # Vérifier que chaque élément est un float
                        if all(isinstance(i, float) for i in data_content):
                            # Préparer la structure de données à encoder
                            data_to_send = f"{_pcs.codes[order_code][0]}|{data_content}"
                            data = data_to_send.encode('utf8')

                            self.socket.send(data)
                            print(f"Data sent: {data}")
                            # Ici, nous n'encode pas encore, juste une préparation
                        else:
                            print(f"\033[31mLe type des éléments du tuple n'est pas correct,\033[34m type(data_content): {type(data_content)}\033[0m")
                    else:
                        print(f"\033[31mLe type de donnée fournie n'est pas correcte,\033[34m type(data_content): {type(data_content)}\033[0m")

    def execute_order(self, order_code):
        if order_code == _pcs.codes["Ping"]:
            print("Ping reçu")
            self.send_order("Pong")

    def start(self):
        self.send_order("PlayerConnect")
        self.send_order("PositionPlayer", (25.2, 59.3))

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
