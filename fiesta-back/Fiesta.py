from Notebook import Notebook
import numpy as np

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
        self.notebooks = []
        self.current_turn = 0

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

    def add_word_from_sid(self, word, sid):
        notebook = self.get_notebook_from_sid(sid)
        notebook.add_word(word)

    def get_next_player_sid(self, sid):
        current_sid_index = np.where(self.ordered_sid== sid)[0][0]
        next_sid_index = self.ordered_sid[(current_sid_index+1)%len(self.players)]
        return next_sid_index

    def get_previous_player_sid(self, sid):
        current_sid_index = np.where(self.ordered_sid== sid)[0][0]
        previous_sid_index = self.ordered_sid[(current_sid_index-1)]
        return previous_sid_index

    def get_last_word_from_sid(self, sid):
        notebook = self.get_notebook_from_sid(sid)
        return notebook.words[-1]

    def cycle_notebooks(self):
        for notebook in self.notebooks:
            previous_sid = self.get_previous_player_sid(notebook.sid)
            notebook.sid = previous_sid

    def start_round(self):
        order = np.arange(len(self.players))
        np.random.shuffle(order)
        self.ordered_sid = np.array(list(self.players.keys()))[order]
        for sid in self.ordered_sid:
            self.notebooks.append(
                Notebook(sid))

    def get_notebook_from_sid(self, sid):
        for notebook in self.notebooks:
            if sid == notebook.sid:
                return notebook

    def check_if_all_ready(self):
        """ Checks if all players are ready
        Returns
        ----------
        all_ready
            boolean
        """
        all_ready = True
        for sid in self.players:
            all_ready &= self.players[sid]['ready']
        return all_ready

    def check_if_all_words_submitted(self):
        """ Checks if all players are ready
        Returns
        ----------
        all_words_submitted
            boolean
        """
        all_words_submitted = True
        for notebook in self.notebooks:
            word_submitted = (len(notebook.words) == 2 + self.current_turn)
            all_words_submitted &= word_submitted
        return all_words_submitted   

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
