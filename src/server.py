# coding:utf-8

import socket
import time
import threading
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
        # Définir le tick rate
        TICK_RATE = 30  # 30 Hz, mise à jour toutes les 33 ms
        self.TICK_INTERVAL = 1 / TICK_RATE  # Intervalle entre les mises à jour

        # Boucle principale du serveur
        last_time = time.time()

        while True:
            try:
                data, address = self.socket.recvfrom(1024)  # Réception des données
                data = data.decode('utf-8')

                client_thread = ThreadForClient(self, address, data)
                client_thread.start()
            except Exception as e:
                print(f"Erreur lors de la réception des données : {e}")

            self.limit_refresh(last_time)


    def limit_refresh(self, last_time):
        # Temps actuel
        current_time = time.time()

        # Calculer le temps écoulé depuis la dernière mise à jour
        delta_time = current_time - last_time

        if delta_time >= self.TICK_INTERVAL:
            # Logic du serveur : traitement de la mise à jour
            print(f"Serveur mis à jour à {current_time:.3f}")

            # Mettre à jour last_time
            last_time = current_time

        # Optimisation : attente pour ne pas trop solliciter le processeur
        time.sleep(0.001)  # Petite pause pour limiter la charge CPU


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
            code_and_players_pos = f"PPos, {data_base.player_pos}"
            self.server.send_data_to_clients(code_and_players_pos)

#----------------------------------------------------------------
if __name__ == "__main__":
    server = Server()
    server.listen()
