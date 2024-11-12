# coding:utf-8

import socket
import threading
import time
import protocolClientServer as _pcs
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

#----------------------------------------------------------------
@dataclass
class DataBase:
    """les données du serveur"""
    host: str = '0.0.0.0'
    port: int = 49352
    clients: List[Tuple[str, int]] = field(default_factory=list)

    # Informations des joueurs
    player_name: Dict[str, str] = field(default_factory=dict)  # Format : {ip: name}
    player_pos: Dict[Tuple[str, int], Tuple[float, float]] = field(default_factory=dict)  # Format : {(ip, port): (x, y)}

data_base = DataBase()

class Server:

    def __init__(self):
        host = data_base.host
        port = data_base.port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Utiliser UDP
        self.socket.bind((host, port))  # Associer à l'adresse et au port

        # Obtenir l'adresse IP du serveur
        hostname = socket.gethostname()
        hostname = socket.gethostbyname(hostname)

        print(f"Le serveur est démarré sur {hostname}:{port}")

        self.game_data_sender = GameDataSender(self)
        self.game_data_sender.start()

    def listen(self):
        """Écoute et traite les messages des clients."""
        while True:
            try:
                data, address = self.socket.recvfrom(1024)  # Réception des données
                data = data.decode('utf-8')
                print(f"Message reçu de {address}: {data}")

                client_thread = ThreadForClient(self, address, data)
                client_thread.start()
            except Exception as e:
                print(f"Erreur lors de la réception des données : {e}")

    def send_data_to_clients(self, data):
        """Envoie les données à tous les clients."""
        data = data.encode("utf-8")

        for client_address in data_base.clients:
            try:
                self.socket.sendto(data, client_address)
            except Exception as e:
                print(f"Erreur lors de l'envoi des données à {client_address}: {e}")

class ThreadForClient(threading.Thread):

    def __init__(self, server, address, data):
        super().__init__()
        self.server = server
        self.address = address
        self.data = data

    def run(self):
        """Gère la communication avec le client."""
        self.execute_order(self.data)

    def execute_order(self, data):
        """Exécute les différentes commandes en fonction des données reçues."""
        if data == _pcs.codes["PlayerDisconnect"]:
            self.remove_client()
            print(f"Client {self.address} a demandé la déconnexion.")
        elif data == _pcs.codes["PlayerConnect"]:
            self.register_client()
        else:
            order_code, content_string = data.split('|')

            if order_code == _pcs.codes["PositionPlayer"][0]:  # "PPos"
                position_string = content_string.strip('()')
                position = tuple(map(float, position_string.split(',')))

                # Enregistrer la position du joueur
                data_base.player_pos[self.address] = position
            else:
                print("\033[31m" + f"L'ordre reçu n'est pas géré: {order_code}" + "\033[0m")

    def register_client(self):
        """Enregistre le client si ce n'est pas déjà fait."""
        if self.address not in data_base.clients:
            data_base.clients.append(self.address)
            print(f"Client {self.address} connecté.")

    def remove_client(self):
        """Supprime un client."""
        if self.address in data_base.clients:
            data_base.clients.remove(self.address)
            data_base.player_pos.pop(self.address, None)
            print(f"Client {self.address} est déconnecté")

class GameDataSender(threading.Thread):

    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        self.regroup_data()

    def regroup_data(self):
        """Envoie les données importantes aux clients."""
        while True:
            time.sleep(0.015)
            code_and_players_pos = f"PPos, {data_base.player_pos}"
            self.server.send_data_to_clients(code_and_players_pos)

#----------------------------------------------------------------
if __name__ == "__main__":
    server = Server()
    server.listen()
