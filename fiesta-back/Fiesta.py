import Notebook

class Fiesta():
    """Fiesta game state class.

    The fiesta class stores and manages the state of the game.
    Players data are also managed here.

    Attributes
    ----------
    connections
        List of session ids
    players
        List of player dictionnaries

    """
    def __init__(self):
        self.connections = []
        self.players = {}

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
        if sid in self.players:
                exists = True
        if not exists:
            self.players[sid] = {'nickname' : nickname, 'ready' : False}

    def set_ready(self, ready, sid):
        """ Sets ready status of player.
        Attributes
        ----------
        ready
            boolean
        sid
            session id of the connection
        """
        self.players[sid]['ready'] = ready

    def check_if_all_ready(self):
        """ Checks if all players are ready
        Returns
        ----------
        all_ready
            boolean
        """
        all_ready = False
        for sid in self.players:
            all_ready |= self.players[sid]['ready']
        return all_ready

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
