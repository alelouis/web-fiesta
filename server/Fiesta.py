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
    """Notebook of Fiesta game.

    The Notebook class emulates a physical notebook belonging to a player.

    Attributes
    ----------
    player
        owner of the notebook
    drawing
        list of rounds drawings
    drawing
        list of rounds words
    round
        current round of the notebook

    """
    def __init__(self, owner):
        self.player = player
        self.drawings = []
        self.words = []
        self.round = 0
    
    def add_word(self, word):
        """ Adds a word to the notebook and increments round.
        Attributes
        ----------
        word
            string of written word
        """
        self.words.append({self.round : word})
        self.round += 1

    def add_drawing(self, drawing):
        """ Adds a drawing to the notebook and increments round.
        Attributes
        ----------
        drawing
            drawing data
        """
        self.words.append({self.round : drawing})
        self.round += 1
