from client import Client

class InternetManager:

    def start(self, game):
        """Lance la synchronisation client server"""
        self.client_thread = Client(game)
        self.client_thread.start()

        self.my_ip = self.client_thread.get_my_id()  # recupère et stock l'ip public du client


    def stop(self):
        """Arrete la synchronisation client server"""
        if self.client_thread.is_alive():
            self.client_thread.is_connected = False

    def get_players_position(self) -> tuple[float, float]:
        """Renvoie la position du joueur local et des autres joueurs"""
        local_player_pos = None
        all_players_pos = []

        for data in self.client_thread.get_players_position():
            ip, coords = data

            if ip == self.my_ip:
                local_player_pos = coords

            all_players_pos.append((ip, coords))

        return local_player_pos, all_players_pos


    def force_update(self):
        try:
            if self.client_thread.is_connected and not self.client_thread.socket._closed:
                self.client_thread.send_update()
        except Exception as e:
            print(f"Erreur dans force_update(): {e}")
            if not self.client_thread.socket._closed:
                self.client_thread.socket.close()