# coding:utf-8
"""
    TODO: 
        actualiser en temps reel les coordonées du joueur
        actualiser les coordonées des autres joueurs
"""

import socket
import threading
import requests
import ast
import protocolClientServer as _pcs
from dataclasses import dataclass, field
from typing import Dict, Tuple

host, port = ('89.168.57.22', 49352)

@dataclass
class DataBase:
    player_pos: Dict[Tuple[str, int], Tuple[float, float]] = field(default_factory=dict)  # Format : {(ip, port): (x, y)}


data_base = DataBase()


class Client(threading.Thread):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.is_connected = True
        self.lock = threading.Lock()

        print("Lancement de la connexion au serveur...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Créer le socket
        self.socket.settimeout(0.5)  # ajoute un timeout pour eviter le bloquage

        try:
            self.socket.connect((host, port))  # Connecter le socket
            print("Client connecté !")
        except Exception as e:
            print(f"Connexion au serveur échouée ! Erreur: {e}")
            self.socket.close()  # Fermer le socket en cas d'échec de connexion


    def get_players_position(self):
        return list(data_base.player_pos.items())  # list() pour transformer le dic en list // .items() pour recupere a la fois la clé mais aussi la donnée

    def get_my_id(self):
        """Recupère l'ip public et le port du client"""
        ip = requests.get("https://api.ipify.org?format=text").text  # Récupère l'IP publique
        port = self.socket.getsockname()[1]  # Récupère le port local utilisé pour communiquer avec le serveur
        return (ip, port)

    def get_socket(self):
        return self.socket



    def format_data_without_content(self, order_code):
        """Format et envoie les codes au server"""
        data = _pcs.codes[order_code].encode('utf8')
        self.socket.send(data)  # Utiliser send au lieu de sendto

    def format_data_with_content(self, order_code, content):
        """Format et envoie les codes et les données au server"""
        if order_code == "PositionPlayer":
            # Vérification si data_content est un tuple de deux floats
            if isinstance(content, tuple) and len(content) == 2:
                # Préparer la structure de données à encoder
                data_to_send = f"{_pcs.codes[order_code][0]}|{content}"
                data = data_to_send.encode('utf8')

                self.socket.send(data)
            else:
                print(f"\033[31mLe type de donnée fournie n'est pas correcte,\033[34m type(data_content): {type(content)}\033[0m")

    def send_order(self, order_code, data_content=None):
        """Logique de formatage et d'envoie des données"""
        if order_code in _pcs.codes:
            # si aucune donnée n'est donnée, considerer qu'il n'y en a pas a donner
            if not data_content:
                self.format_data_without_content(order_code)
            else:
                self.format_data_with_content(order_code, data_content)


    def execute_order(self, data_received):
        """Extrès le code et les données puis execute l'ordre adequate"""  # oui je sais pas écrire mais oklm demande a chatgpt
        order_code, data_content_str = data_received.split(", ", 1)  # Séparer le code du reste

        if order_code == _pcs.codes["PositionPlayer"][0] and data_content_str:
            data_content = ast.literal_eval(data_content_str)  # Convertir la chaîne en dictionnaire

            # Vérifier si le dictionnaire est vide
            if data_content:  # Si data_content n'est pas vide, on continue
                data_content = list(data_content.items())  # transforme data_content en liste pour pouvoir travailler dessus plus facilement

                data_base.player_pos.clear()  # reset la position de tout les jouers pour supprimer ceux qui ne sont plus co

                for data in data_content:
                    ip_port, coords = list(data)  # Extraire la clé et les coordonnées
                    data_base.player_pos[ip_port] = coords  # met a jour dans la base de données


    def disconnect(self):
        self.send_order("PlayerDisconnect")
        self.socket.close()  # Fermer le socket

    def connect(self):
        self.send_order("PlayerConnect")


    def send_update(self):
        """Envoie l'ensemble des données utiles a actualiser le jeu"""
        self.send_player_position()

    def send_player_position(self, position=None, send=True):
        """Envoie la position du joueur"""
        if position:
            player_position = position  # Si une position est fournie, on la utilise
        else:
            player_position = self.game.player.position

        if send:
            self.send_order("PositionPlayer", player_position)
        else:
            return player_position


    def get_order(self):
        """Recupère toutes les données envoyers"""
        data = self.socket.recv(1024).decode('utf8')  # Recevoir des données du serveur

        if data:
            self.execute_order(data)  # Traiter les données reçues


    def run(self):
        """Boucle d'actualisation"""
        self.connect()

        while self.is_connected:
            try:
                self.get_order()
            except socket.timeout:
                pass
            except Exception as e:
                print(f"Erreur dans get_order(): {e}")
                self.socket.close()
                break

            try:
                self.send_update()
            except Exception as e:
                print(f"Echec de l'envoie des données : {e}")