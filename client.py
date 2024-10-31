# coding:utf-8

"""
    TODO: 
        prise en charge des vrai coordonées du joueur
        actualiser en temps reel les coordonées du joueur
        actualiser les coordonées des autres joueurs
"""

import socket
import threading
import time
import protocolClientServer as _pcs
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

host, port = ('89.168.57.22', 49352)

@dataclass
class DataBase:
    PlayerPosition: Tuple[float, float] = field(default_factory=tuple)  # Format :(x, y)

class Client(threading.Thread):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.is_connected = True

        print("Lancement de la connexion au serveur...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Créer le socket
        self.socket.settimeout(0.05)  # ajoute un timeout pour eviter le bloquage

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

                            print(f"Data sent: {data}")
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

    def disconnect(self):
        self.send_order("PlayerDisconnect")
        self.socket.close()  # Fermer le socket

    def connect(self):
        self.send_order("PlayerConnect")

    def send_update(self):
        player_position = self.game.player.position
        self.send_order("PlayerPosition", player_position)

    def get_order(self):
        data = self.socket.recv(1024).decode('utf8')  # Recevoir des données du serveur

        if data:
            print(f"Données reçues: {data}")
            self.execute_order(data)  # Traiter les données reçues

    def run(self):
        self.connect()

        while self.is_connected:
            print("ok")
            try:
                self.get_order()
                print("Order received")  # Pour voir si get_order() passe correctement
            except socket.timeout:
                print("Aucune donnée reçue (timeout), en attente...")
            except Exception as e:
                print(f"Erreur dans get_order(): {e}")
                self.socket.close()
                break

            try:
                self.send_update()
                print("Update sent")  # Pour voir si send_update() passe correctement
            except Exception as e:
                print(f"Erreur dans send_update(): {e}")
                self.socket.close()
                break

#----------------------------------------------------------------
# client = Client()
# client.run()