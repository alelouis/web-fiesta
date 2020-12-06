import sys

from flask_cors.core import get_allow_headers
sys.path.append('.')
import Fiesta

fiesta = Fiesta.Fiesta()
players = ['John', 'Bob', 'Alice', 'Doe']
sids = ['1', '2', '3', '4']

def test_player_creation():
    for i, player in enumerate(players):
        fiesta.add_player(player, sids[i])
    assert len(fiesta.players) == len(players)

def test_check_ready():
    assert fiesta.check_if_all_ready() == False
    for sid in sids:
        fiesta.set_ready(True, sid)
    assert fiesta.check_if_all_ready() == True

def test_round_started():
    fiesta.start_round()
    assert len(fiesta.notebooks) == len(fiesta.players)
    assert len(fiesta.ordered_sid) == len(fiesta.players)

def test_add_words():
    for sid in sids:
        fiesta.add_word_from_sid(str(sid) + '_' + str(fiesta.current_turn), sid)
    for notebook in fiesta.notebooks:
        assert len(notebook.words) == 2

def test_notebook_cycling():
    n_sids = len(fiesta.players)
    sids_before = []
    for notebook in fiesta.notebooks:
        sids_before.append(notebook.sid)

    fiesta.cycle_notebooks()

    sids_after = []
    for notebook in fiesta.notebooks:
        sids_after.append(notebook.sid)
    
    for s in range(n_sids):
        assert sids_before[s] == sids_after[(s+1)%n_sids]

def test_get_all_characters():
    characters = fiesta.get_all_characters()
    assert len(characters) == 8

def test_get_all_last_words():
    last_words = fiesta.get_all_last_words()
    assert len(last_words) == len(fiesta.players)

def test_correction():
    notebook = fiesta.notebooks[0]
    fiesta.process_answers('1', {notebook.words[-1] : 'character'})
    fiesta.process_answers('2', {notebook.words[-1] : notebook.character})
    fiesta.process_answers('3', {notebook.words[-1] : 'character'})
    fiesta.process_answers('4', {notebook.words[-1] : notebook.character})
    corrections = fiesta.get_corrections(fiesta.notebooks[0])
    assert len(corrections) == len(fiesta.players)

def test_bone():
    notebook = fiesta.notebooks[1]
    fiesta.process_answers('1', {notebook.words[-1] : notebook.character})
    fiesta.process_answers('2', {notebook.words[-1] : notebook.character})
    fiesta.process_answers('3', {notebook.words[-1] : notebook.character})
    fiesta.process_answers('4', {notebook.words[-1] : notebook.character})
    corrections = fiesta.get_corrections(fiesta.notebooks[1])
    assert fiesta.bones == 1