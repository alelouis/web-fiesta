import sys
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
