import Fiesta

fiesta = Fiesta.Fiesta()

fiesta.add_player('Alexis', '1234')
fiesta.add_player('Nico', '5678')
fiesta.add_player('Camille', '1324')
fiesta.add_player('Margot', '5768')

fiesta.set_ready(True, '1234')
fiesta.set_ready(False, '5678')
fiesta.set_ready(True, '1324')
fiesta.set_ready(False, '5768')

fiesta.start_round()

fiesta.add_word_from_sid('grenouille', '1234')
fiesta.add_word_from_sid('renard', '5678')

fiesta.add_word_from_sid('elephant', '1324')
fiesta.add_word_from_sid('licorne', '5768')

for notebook in fiesta.notebooks:
    print(notebook.sid)
    print(notebook.words)
fiesta.cycle_notebooks()


print("Next for '1234' %s"%fiesta.get_last_word_from_sid('1234'))
print("Next for '5678' %s"%fiesta.get_last_word_from_sid('5678'))
print("Next for '1324' %s"%fiesta.get_last_word_from_sid('1324'))
print("Next for '5768' %s"%fiesta.get_last_word_from_sid('5768'))



for notebook in fiesta.notebooks:
    print(notebook.sid)
    print(notebook.words)