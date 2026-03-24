class PlayerManager:
    def __init__(self):
        self.players = {}

    def add_player(self, player_id, player_name):
        self.players[player_id] = player_name

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]

    def get_player(self, player_id):
        return self.players.get(player_id, None)

    def list_players(self):
        return self.players
