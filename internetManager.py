from client import Client

class InternetManager:

    def start(self, game):
        """Lance la synchronisation client server"""
        self.client_thread = Client(game)
        self.client_thread.start()

        self.my_ip = self.client_thread.get_my_ip()  # recupère et stock l'ip public du client

    def stop(self):
        """Arrete la synchronisation client server"""
        if self.client_thread.is_alive():
            self.client_thread.disconnect()  # Déconnexion propre
            self.client_thread.join()  # Attendre que le thread se termine

    def get_players_position(self) -> tuple[float, float]:
        """Renvoie la position du joueur local et des autres joueurs"""
        local_player_pos = None
        oser_players_pos = []

        for data in self.client_thread.get_players_position():
            ip, coords = data

            if ip == self.my_ip:
                local_player_pos = coords
                continue
            else:
                oser_players_pos.append((ip, coords))

        return local_player_pos, oser_players_pos