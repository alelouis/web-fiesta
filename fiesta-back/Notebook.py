import random

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
        with open('characters', encoding="utf8") as f:
            characters_list = f.read().splitlines()
        self.character = random.choice(characters_list)
        self.sid = sid
        self.words = [self.character]
        self.correct_answers = 0

    def add_word(self, word):
        """ Adds a word to the notebook and increments round.
        Attributes
        ----------
        word
            string of written word
        """
        self.words.append(word)


