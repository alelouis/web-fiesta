
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
    def __init__(self, player):
        self.player = player
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

