import argparse
import requests
from bs4 import BeautifulSoup
import json
import re

# Draftkings EPL data

dk_EPL_url = 'https://sportsbook.draftkings.com/leagues/soccer/england---premier-league'

dk_r = requests.get(dk_EPL_url)
dk_status = dk_r.status_code
print('dk_status=', dk_status)
dk_html = dk_r.text

dk_soup = BeautifulSoup(dk_html, 'html.parser')

# Pulls span tags than includes the betting odds and converts it into a string
dk_span_tags = dk_soup.find_all('span', class_= 'sportsbook-odds american default-color')
dk_str_span_tags = []
for item in dk_span_tags:
    dk_str_span_tags.append(str(item))

# Creates a string of the current odds
dk_odds = []
for dk_tag in dk_str_span_tags:
    result = re.search('>(.*?)<', dk_tag).group(1)
    dk_odds.append(result)

# print(dk_odds)

# Changes casino odds into multiples
dk_multi_odds = []
for dk_odd in dk_odds:
    if dk_odd[0] == '+':
        dk_multi_pos_result = int(dk_odd[1:])/100
        dk_multi_odds.append(dk_multi_pos_result)
    else:
        dk_multi_neg_result = 100 / int(dk_odd[1:])
        dk_multi_neg_result_rounded = round(dk_multi_neg_result, 4)
        dk_multi_odds.append(dk_multi_neg_result_rounded)

# print(dk_multi_odds)

# Converting the master list into home, draw, and away lists
dk_home_odds = [dk_multi_odds[i] for i in range(0, len(dk_multi_odds), 3)]
dk_draw_odds = [dk_multi_odds[i] for i in range(1, len(dk_multi_odds), 3)]
dk_away_odds = [dk_multi_odds[i] for i in range(2, len(dk_multi_odds), 3)]

# print(dk_home_odds)
# print(dk_draw_odds)
# print(dk_away_odds)

# Extract the match name
dk_game_tags = dk_soup.find_all('a', {'class' : 'sportsbook-event-accordion__title'})
dk_str_game_tags = []
for link in dk_game_tags:
   dk_str_game_tags.append(str(link.get('href')))

dk_games = []
for item in dk_str_game_tags:
    start = item.find('/') + 7  # Find the index of the first '/'
    end = item.rfind('/')  # Find the index of the last '/'
    result = item[start:end]
    dk_games.append(result)

# print(dk_games)

# Builds Draftkings EPL dictionary
dk_dictionary = {game: [home, draw, away] for game, home, draw, away in zip(dk_games, dk_home_odds, dk_draw_odds, dk_away_odds)}

print(dk_dictionary)



