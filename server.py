# coding:utf-8

"""
    TODO:
        mettre en bleu clair les nouvelles connection et en bleu foncé les déconnections
"""

import socket
import threading
import time
import protocolClientServer as _pcs
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

#----------------------------------------------------------------
@dataclass
class DataBase:
    """Les données du serveur"""
    host: str = '0.0.0.0'
    port: int = 49352
    clients: List[Tuple[str, int]] = field(default_factory=list)  # liste des adresses clients

    # Informations des joueurs
    player_name: Dict[str, str] = field(default_factory=dict)  # Format : {ip: name}
    player_pos: Dict[Tuple[str, int], Tuple[float, float]] = field(default_factory=dict)  # Format : {(ip, port): (x, y)}

data_base = DataBase()

class Server:

    def __init__(self):
        host = data_base.host
        port = data_base.port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Créer le socket en UDP
        self.socket.bind((host, port))  # Associe à l'adresse et le port

        # Obtenir l'adresse IP du serveur
        hostname = socket.gethostname()
        hostname_ip = socket.gethostbyname(hostname)

        print(f"Le serveur est démarré sur {hostname_ip}:{port}")

        self.game_data_sender = GameDataSender(self)
        self.game_data_sender.start()

    def send_data_to_clients(self, data):
        """Envoie les données à tous les clients"""
        data = data.encode("utf-8")
        for client_addr in data_base.clients:
            try:
                self.socket.sendto(data, client_addr)  # Envoie les données à chaque adresse client
            except Exception as e:
                print(f"Erreur lors de l'envoi des données au client {client_addr}: {e}")

    def listen(self):
        """Écoute les messages des clients"""
        while True:
            try:
                data, address = self.socket.recvfrom(1024)  # Reçoit les données et l'adresse de chaque client
                print(f"Information reçue de {address}")

                if address not in data_base.clients:
                    data_base.clients.append(address)  # Enregistre le client
                    print(f"\033[94mClient {address} connecté.\033[0m")

                client_thread = ThreadForClient(self, data, address)
                client_thread.start()

            except Exception as e:
                print(f"Erreur lors de la réception des données: {e}")

class ThreadForClient(threading.Thread):

    def __init__(self, server, data, address):
        super().__init__()
        self.server = server
        self.data = data.decode("utf-8")
        self.address = address

    def run(self):
        """Gère la communication avec le client"""
        self.execute_order(self.data)

    def execute_order(self, data):
        """Exécute les commandes selon les données reçues"""
        if data == _pcs.codes["PlayerDisconnect"]:
            self.remove_client()
            print(f"\033[34mClient {self.address} a demandé la déconnexion.\033[0m")
        elif data == _pcs.codes["PlayerConnect"]:
            self.register_client()
        else:
            order_code, content_string = data.split('|')

            if order_code == _pcs.codes["PositionPlayer"][0]:  # "PPos"
                position_string = content_string.strip('()')
                position = tuple(map(float, position_string.split(',')))
                data_base.player_pos[self.address] = position  # Enregistre la position du joueur
            else:
                print(f"\033[31mL'ordre reçu n'est pas géré: {order_code}\033[0m")

    def register_client(self):
        """Enregistre le client s'il n'est pas déjà connecté"""
        if self.address not in data_base.clients:
            data_base.clients.append(self.address)
            print(f"\033[94mClient {self.address} connecté.\033[0m")

    def remove_client(self):
        """Supprime un client"""
        if self.address in data_base.clients:
            data_base.clients.remove(self.address)
            data_base.player_pos.pop(self.address, None)
            print(f"\033[34mClient {self.address} est déconnecté.\033[0m")

class GameDataSender(threading.Thread):

    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        self.regroup_data()

    def regroup_data(self):
        """Envoie les données importantes aux clients"""
        while True:
            time.sleep(0.1)  # Evite la surcharge

            code_and_players_pos = f"PPos, {data_base.player_pos}"
            self.server.send_data_to_clients(code_and_players_pos)

#----------------------------------------------------------------
if __name__ == "__main__":
    server = Server()
    server.listen()
