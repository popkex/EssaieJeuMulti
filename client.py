# coding:utf-8
import pygame
import socket
import threading
import requests
import ast
import re
import protocolClientServer as _pcs
from dataclasses import dataclass, field
from typing import Dict, Tuple

host, port = ('89.168.57.22', 49352)

@dataclass
class DataBase:
    player_pos: Dict[Tuple[str, int], Tuple[float, float]] = field(default_factory=dict)

data_base = DataBase()

class Client(threading.Thread):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.is_connected = True
        self.clock = pygame.time.Clock()

        print("Lancement de la connexion au serveur...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Utiliser UDP
        self.socket.settimeout(0.5)

        # Pas de connexion explicite pour UDP
        print("Client prêt à envoyer et recevoir des messages UDP.")

    def get_players_position(self):
        return list(data_base.player_pos.items())

    def get_my_id(self):
        """Récupère l'IP publique et le port local du client"""
        ip = requests.get("https://api.ipify.org?format=text").text
        port = self.socket.getsockname()[1]
        return (ip, port)

    def get_socket(self):
        return self.socket

    def format_data_without_content(self, order_code):
        """Format et envoie les codes au serveur"""
        data = _pcs.codes[order_code].encode('utf8')
        self.socket.sendto(data, (host, port))

    def format_data_with_content(self, order_code, content):
        """Format et envoie les codes et les données au serveur"""
        if order_code == "PositionPlayer":
            if isinstance(content, tuple) and len(content) == 2:
                data_to_send = f"{_pcs.codes[order_code][0]}|{content}"
                data = data_to_send.encode('utf8')
                self.socket.sendto(data, (host, port))
            else:
                print(f"\033[31mLe type de donnée fourni n'est pas correct,\033[34m type(content): {type(content)}\033[0m")

    def send_order(self, order_code, data_content=None):
        """Logique de formatage et d'envoi des données"""
        if order_code in _pcs.codes:
            if not data_content:
                self.format_data_without_content(order_code)
            else:
                self.format_data_with_content(order_code, data_content)

    def execute_order(self, data_received):
        """Extrait le code et les données puis exécute l'ordre adéquat"""
        order_code, data_content_str = data_received.split(", ", 1)

        match = re.search(r"(\{.+?\})", data_content_str)
        
        if match:
            data_content_str = match.group(1)

            try:
                data_content = ast.literal_eval(data_content_str)
            except (SyntaxError, ValueError) as e:
                print(f"Erreur de parsing des données: {e}")
                return

            if data_content:
                data_content = list(data_content.items())

                if order_code == _pcs.codes["PositionPlayer"][0]:
                    data_base.player_pos.clear()

                    for data in data_content:
                        ip_port, coords = data
                        data_base.player_pos[ip_port] = coords
        else:
            print("Erreur : aucune donnée 'PPos, { ... }' trouvée dans data_received")

    def disconnect(self):
        self.send_order("PlayerDisconnect")
        self.socket.close()

    def connect(self):
        self.send_order("PlayerConnect")

    def send_update(self):
        """Envoie l'ensemble des données utiles pour actualiser le jeu"""
        self.send_player_position()

    def send_player_position(self, position=None, send=True):
        """Envoie la position du joueur"""
        player_position = position if position else self.game.player.position

        if send:
            self.send_order("PositionPlayer", player_position)
        else:
            return player_position

    def get_order(self):
        """Récupère toutes les données envoyées"""
        try:
            data, addr = self.socket.recvfrom(1024)
            data = data.decode('utf8')

            if data:
                self.execute_order(data)
        except socket.timeout:
            pass
        except Exception as e:
            print(f"Erreur dans get_order(): {e}")

    def run(self):
        """Boucle d'actualisation"""
        self.connect()

        while self.is_connected:
            try:
                self.get_order()
            except Exception as e:
                print(f"Erreur dans get_order(): {e}")
                self.socket.close()
                break

            try:
                self.send_update()
            except Exception as e:
                print(f"Echec de l'envoi des données : {e}")

            self.clock.tick(60)