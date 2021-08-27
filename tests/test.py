from splinter import Browser

players = ['Nicolas', 'Alexis', 'Jean-Michel']
browsers = {}

for e, player in enumerate(players):
    browser = Browser('firefox')
    browser.driver.set_window_size(600, 800)
    browser.driver.set_window_position(20 + 600 * e, 500)
    browser.visit('http://localhost:4200')
    browsers[player] = browser

for player in players:
    browsers[player].find_by_id('mat-input-0').type(player)
    browsers[player].find_by_text('Rejoindre').click()

for player in players:
    browsers[player].find_by_id('mat-slide-toggle-1').click()

for i in range(1,5):
    for player in players:
        browsers[player].find_by_id(f'mat-input-{i}').type(f'{player}_reply_round_{i}')
        browsers[player].find_by_tag('button').click()