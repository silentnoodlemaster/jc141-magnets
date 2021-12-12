from game import Game
import leet
from concurrent.futures import ThreadPoolExecutor

leet = leet.Leet()
games = leet.get_json()

rows = [("name","date","url","magnet")]

def append_row(game):
  g = Game(game["url"])
  rows.append((game["name"],game["date"], game["url"], g.magnet))

with ThreadPoolExecutor(max_workers=1000) as executor:
  executor.map(append_row, [game for game in games])

with open('johncena141.csv', 'w') as f:
  for magnet in rows:
    f.write('"' + '","'.join(magnet) + '"\n')

