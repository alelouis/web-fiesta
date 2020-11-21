import Fiesta

fiesta = Fiesta.Fiesta()

players = ['John', 'Bob', 'Alice', 'Doe']
sids = ['1', '2', '3', '4']
for i, player in enumerate(players):
    fiesta.add_player(player, sids[i])

for sid in sids:
    fiesta.set_ready(True, sid)

fiesta.start_round()

for sid in sids:
    fiesta.add_word_from_sid(str(sid) + '_' + str(fiesta.current_turn), sid)

for sid in sids:
    word = fiesta.get_last_word_from_sid(sid)

print(str(fiesta))
