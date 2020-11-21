import numpy as np

class Notebook():
    """Notebook of Fiesta game.

    The Notebook class emulates a physical notebook belonging to a player.

    Attributes
    ----------
    player
        owner of the notebook
    words
        list of rounds words
    round
        current round of the notebook

    """
    def __init__(self, sid):
        # TODO : Sampling sans remise
        characters = ['cheval', 'loutre', 'dauphin', 'chien', 'chat', 'lamasticot', 'puceron']
        self.character = np.random.choice(characters)
        self.sid = sid
        self.words = [self.character]

    def add_word(self, word):
        """ Adds a word to the notebook and increments round.
        Attributes
        ----------
        word
            string of written word
        """
        self.words.append(word)

