from client import Client

class InternetManager:

    def start(self, game):
        """Lance la synchronisation client server"""
        self.client_thread = Client(game)
        self.client_thread.start()

    def stop(self):
        """Arrete la synchronisation client server"""
        if self.client_thread.is_alive():
            self.client_thread.disconnect()  # Déconnexion propre
            self.client_thread.join()  # Attendre que le thread se termine