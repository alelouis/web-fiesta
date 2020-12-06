from Notebook import Notebook
import logging
import sys
import random

class Fiesta():
    """Fiesta game state class.

    The fiesta class stores and manages the state of the game.
    Players data are also managed here.

    Attributes
    ----------
    players
        List of player dictionnaries {'nickname', 'sid'}
    notebooks
        List of notebooks containing words and characters
    current_turn
        turn count

    """
    def __init__(self):
        # Game
        self.players = {}
        self.notebooks = []
        self.current_turn = 0
        self.sampled_characters = []
        self.bones = 0
        self.constraint_level = 1
        self.constraints = []

        # Logging
        self.log = logging.getLogger("fiesta")
        formatter = logging.Formatter('%(asctime)s - %(name)8s - [%(levelname)s] %(message)s')

        fh = logging.FileHandler('logs/fiesta.log')
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)

        self.log.addHandler(fh)
        self.log.setLevel(logging.DEBUG)

        self.log.info("Fiesta game initilized.")

# state

    def cycle_notebooks(self):
        """ Move notebooks along players."""
        self.log.info("Cycling notebooks.")
        for notebook in self.notebooks:
            previous_sid = self.get_previous_player_sid(notebook.sid)
            notebook.sid = previous_sid
    
    def clear_game(self):
        """ Resets game state."""
        self.log.info("Resetting game state.")
        self.notebooks = []
        self.current_turn = 0
        self.bones = 0
        self.contraints = []
        for sid in self.players:
            self.players[sid]['ready'] = False
            del self.players[sid]['answers']


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
        self.log.debug(f'Player {self.players[sid]} ready status changed to {ready}')

    def start_round(self):
        """ Initialize round.

        - Sets bones number
        - Samples constraints
        - Shuffle player order
         Instanciate and assign notebook to players
        """
        self.log.info("Starting round.")

        # Setting bones number
        self.bones = max(len(self.players) - 4, 0)

        # Sampling constraints
        with open('constraints', encoding="utf8") as f:
            constraints_list = f.read().splitlines()
        for _ in range(self.constraint_level):
            self.constraints.append(random.choice(constraints_list)) 

        # Reordering players
        order = list(range(len(self.players)))
        random.shuffle(order)
        sids = list(self.players.keys())
        self.ordered_sid = [sids[i] for i in order]

        # Assigning notebooks
        for sid in self.ordered_sid:
            new_notebook = Notebook(sid)
            while new_notebook.character in self.sampled_characters:
                new_notebook = Notebook(sid)
            self.sampled_characters.append(new_notebook.character)
            self.notebooks.append(new_notebook)
    
    def process_answers(self, sid, answers):
        self.log.info("Processing answers.")
        self.players[sid]['answers'] = answers

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
        self.log.debug(f"Added word {word} to sid {sid}.")

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
        self.log.info(f"Added player {nickname} of sid {sid} to the game.")

    def add_bone(self):
        """ Adds a bone to game. """
        self.bones += 1

# removers 

    def remove_bone(self):
        """ Removes a bone from the game. """
        self.bones -= 1

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
        current_sid_index = self.ordered_sid.index(sid)
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
        current_sid_index = self.ordered_sid.index(sid)
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

    def get_all_last_words(self):
        """ Gets all last words.
        Return
        -------
        last_words
            list of last words
        """
        self.log.debug("Gets all the last words.")
        last_words = []
        for sid in self.players:
            last_words.append(self.get_last_word_from_sid(sid))
        return last_words

    def get_character(self, sid):
        """ Gets the character of a notebook.
        Attributes
        ----------
        sid
            current player session id
        Return
        -------
        self.character
            character of the notebook
        """
        notebook = self.get_notebook_from_sid(sid)
        return notebook.character

    def get_all_characters(self):
        """ Gets the 8 characters.
        Return
        -------
        characters
            list of shuffled characters
        """
        self.log.debug("Gets all the last words.")
        characters = []
        for notebook in self.notebooks:
            characters.append(notebook.character)
        missing = 8 - len(characters)
        with open('characters', encoding="utf8") as f:
            characters_list = f.read().splitlines()
        characters += list(random.choices(characters_list, k=missing))
        return characters

    def get_corrections(self, notebook):
        """ Gets the corrections for a given notebooks.
        Return
        -------
        corrections
            dictionnary of nickname with bool correction status
        """
        self.log.debug(f"Gets the corrections for notebook with last word {notebook.words[-1]}.")
        corrections = {} 
        last_word = notebook.words[-1]
        for sid in self.players:
            if self.players[sid]['answers'][last_word] == notebook.character:
                corrections[self.players[sid]['nickname']] = True
            else:
                corrections[self.players[sid]['nickname']] = False
        
        self.check_if_all_answers_are_correct(corrections) # Adds bones if necessary
        correct_answers = self.get_number_of_correct_answers(corrections)
        notebook.correct_answers = correct_answers # Set number of correct answers to notebook
        return corrections


    def get_notebook_from_last_word(self, last_word):
        """ Gets a notebook from its last word.
        Attributes
        ----------
        last_word
            last word entered in the notebook
        Return
        -------
        notebook
            notebook with corresponding last word
        """
        for notebook in self.notebooks:
            if notebook.words[-1] == last_word:
                return notebook

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

    def get_number_of_correct_answers(self, corrections):
        """ Gets the number of correct answers
        Attributes
        ----------
        Corrections
            dict of nickname:answers
        Returns
        -------
        correct_answers
            number of correct answers
        """
        correct_answers = 0
        for _, correction in corrections.items():
            correct_answers += correction
        return correct_answers


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
        self.log.debug(f"Check if all players are ready: {all_ready}.")
        return all_ready

    def check_if_all_answers_are_correct(self, corrections):
        """ Checks if all answers are correct in order to give or not a memory bone
        """
        all_correct = True
        for _, correction in corrections.items():
            all_correct &= correction
        if all_correct: 
            self.add_bone()
        self.log.debug(f"Check if all players answers are correct: {all_correct}.")
        return all_correct

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
        self.log.debug(f"Check if all words are submitted: {all_words_submitted}.")
        return all_words_submitted   

    def check_if_all_answers_submitted(self):
        """ Checks if all players submitted their answers
        Returns
        ----------
        all_answers_submitted
            boolean
        """
        self.log.debug(f"Check if all answers are submitted.")
        all_answers_submitted = True
        for sid in self.players:
            answer_submitted = 'answers' in self.players[sid]
            all_answers_submitted &= answer_submitted
        self.log.debug(f"Check if all answers are submitted: {all_answers_submitted}.")
        return all_answers_submitted   

    def check_rotation_completed(self):
        """ Checks the notebook rotation if completed
        Returns
        ----------
        rotation_completed
            boolean
        """
        rotation_completed = (self.current_turn == 4)
        self.log.debug(f"Check if rotation is completed: {rotation_completed}.")
        return rotation_completed