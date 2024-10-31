# coding:utf-8

"""
    TODO:
        mettre en bleu clair les nouvelles connection et en bleufoncer les deconnections
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
    """les données du server"""
    host: str = '0.0.0.0'
    port: int = 49352
    clients_id: List[str] = field(default_factory=list)

    # Informations des joueurs
    player_name: Dict[str, str] = field(default_factory=dict)  # Format : {ip: name}
    player_ip: Dict[str, str] = field(default_factory=dict)    # Format : {name: ip}
    player_pos: Dict[Tuple[str, int], Tuple[float, float]] = field(default_factory=dict)  # Format : {(ip, port): (x, y)}


data_base = DataBase()


# lance le server et recupère toute les données qu'on lui envoie
class Server:

    def __init__(self):
        host = data_base.host
        port = data_base.port
        self.clients_id = data_base.clients_id

        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # créer le socket
        self.socket.bind((host, port))  # s'associe à l'adresse et le port

        # Obtenir l'adresse IP du server
        hostname = socket.gethostname()
        hostname = socket.gethostbyname(hostname)

        print(f"Le serveur est démarré sur {hostname}:{port}")

        self.game_data_sender = GameDataSender(self)
        self.game_data_sender.start()

    def listen(self):
        """Écoute et accepte les connexions des clients."""
        while True:
            self.socket.listen()  # Met en écoute le serveur
            conn, address = self.socket.accept()  # Accepte les connexions
            print(f"Information reçue par un client {address}")

            client_thread = ThreadForClient(self, conn, address)
            client_thread.start()

    def send_data_to_clients(self, data):
        """envoyer les données a un client spécifique (avec sa connection)"""
        data = data.encode("utf-8")

        for client_conn in self.clients_id:
            try:
                client_conn.send(data)  # envoie les données via chaque connexion de client
            except BrokenPipeError as e:
                print(f"error: {e}")



class ThreadForClient(threading.Thread):

    def __init__(self, server, conn, address):
        super().__init__()
        self.server = server
        self.conn = conn
        self.address = address

    def run(self):
        """Gère la communication avec le client."""
        while True:
            try:
                data = self.conn.recv(1024)  # reçoit les données
                if data:
                    data = data.decode('utf8')
                    self.execute_order(data)
            except Exception as e:
                break

        self.remove_client()  # Supprime le client lorsque la communication est interrompue

    def execute_order(self, data):
        """
            Exécute les différentes commandes en fonction des données reçues.
        """
        if data == _pcs.codes["PlayerDisconnect"]:
            self.remove_client()
            print(f"Client {self.address} a demandé la déconnexion.")
        elif data == _pcs.codes["PlayerConnect"]:
            self.register_client()
        else:
            """si l'ordre contient des données"""
            order_code, content_string = data.split('|')  # séprart l'ordre et les données

            if order_code == _pcs.codes["PositionPlayer"][0]:  # "PPos"
                """recupère la position et l'enregistre"""
                position_string = content_string.strip('()')
                position = tuple(map(float, position_string.split(',')))
                data_base.player_pos[self.address] = position  # enregistre la position du joueur
            else:
                print("\033[31m" + f"L'ordre reçu n'est pas géré: {order_code}" + "\033[0m")

    def register_client(self):
        """Enregistre le client si ce n'est pas déjà fait."""
        if self.conn not in self.server.clients_id:
            self.server.clients_id.append(self.conn)  # Ajouter la connexion
            print(f"Client {self.address} connecté.")

    def remove_client(self):
        """Supprime un client"""
        if self.conn in self.server.clients_id:
            self.server.clients_id.remove(self.conn)  # Retirer la connexion
            self.conn.close()  # Fermer la connexion proprement
            data_base.player_pos.pop(self.address, None)
            print(f"Client {self.address} est déconnecté")



class GameDataSender(threading.Thread):

    def __init__(self, server):
        super().__init__()

        self.server = server

    def run(self):
        self.regroup_data()

    def regroup_data(self):
        """Envoie les données importantes aux clients"""
        while True:
            time.sleep(0.05)  # evite la surcharge

            code_and_players_pos = f"PPos, {data_base.player_pos}"
            self.server.send_data_to_clients(code_and_players_pos)

#----------------------------------------------------------------
if __name__ == "__main__":
    server = Server()
    server.listen()