
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
