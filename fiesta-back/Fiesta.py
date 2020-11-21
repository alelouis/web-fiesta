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

# misc.

    def cycle_notebooks(self):
        """ Move notebooks along players."""
        for notebook in self.notebooks:
            previous_sid = self.get_previous_player_sid(notebook.sid)
            notebook.sid = previous_sid

# setters

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

    def start_round(self):
        """ Creates notebooks and randomize player order.
        """
        order = np.arange(len(self.players))
        np.random.shuffle(order)
        self.ordered_sid = np.array(list(self.players.keys()))[order]
        for sid in self.ordered_sid:
            self.notebooks.append(
                Notebook(sid))

# adders 

    def add_word_from_sid(self, word, sid):
        """ Adds a word to a notebook belonging to an sid.
        Attributes
        ----------
        word
            string
        sid
            session id of the connection
        """
        notebook = self.get_notebook_from_sid(sid)
        notebook.add_word(word)

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

# getters 

    def get_next_player_sid(self, sid):
        """ Gets the sid of the next player.
        Attributes
        ----------
        sid
            current player session id
        Return
        -------
        next_sid_index
            next player session id
        """
        current_sid_index = np.where(self.ordered_sid== sid)[0][0]
        next_sid_index = self.ordered_sid[(current_sid_index+1)%len(self.players)]
        return next_sid_index

    def get_previous_player_sid(self, sid):
        """ Gets the sid of the previous player.
        Attributes
        ----------
        sid
            current player session id
        Return
        -------
        next_sid_index
            previous player session id
        """
        current_sid_index = np.where(self.ordered_sid== sid)[0][0]
        previous_sid_index = self.ordered_sid[(current_sid_index-1)]
        return previous_sid_index

    def get_last_word_from_sid(self, sid):
        """ Gets the last word of a notebook.
        Attributes
        ----------
        sid
            current player session id
        Return
        -------
        notebook.words[-1]
            last word of the notebook
        """
        notebook = self.get_notebook_from_sid(sid)
        return notebook.words[-1]

    def get_notebook_from_sid(self, sid):
        """ Gets a notebook from an sid.
        Attributes
        ----------
        sid
            current player session id
        Return
        -------
        notebook
            notebook with corresponding sid
        """
        for notebook in self.notebooks:
            if sid == notebook.sid:
                return notebook

# checks 

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

