class Fiesta():
    """Fiesta game state class.

    The fiesta class stores and manages the state of the game.
    Players data are also managed here.

    Attributes
    ----------
    connected_user
        Number of simultaneous connected users
    n_players
        Number of players

    """
    def __init__(self):
        self.connections = []
        self.players = []
        self.notebook = Notebook('haha')

    def add_player(self, nickname, sid):
        """ Adds new player to the game.
        Attributes
        ----------
        nickname
            Player's nickname
        sid
            session id of the connection
        """
        exists = False
        for player in self.players:
            if sid == player['sid']:
                exists = True
        if not exists:
            self.players.append(new_player)

    def add_connection(self, sid):
        """ Adds new connection to connections list.
        Attributes
        ----------
        sid
            session id of the connection
        """
        self.connections.append(sid)
    
    def remove_connection(self, sid):
        """ Removes connection from connections list.
        Attributes
        ----------
        sid
            session id of the connection
        """
        self.connections.remove(sid)

class Notebook():
    def __init__(self, owner):
        self.owner = owner