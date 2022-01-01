from game import Game
import leet
from concurrent.futures import ThreadPoolExecutor
import csv

leet = leet.Leet()
games = leet.get_json()

rows = [("name","date","size","url","magnet")]

def append_row(game):
  g = Game(game["url"])
  rows.append((game["name"],game["date"], game["size"], game["url"], g.magnet))

with ThreadPoolExecutor(max_workers=1000) as executor:
  executor.map(append_row, [game for game in games])

# Save to CSV
with open('johncena141.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerows(rows)

# Sort by date
with open('johncena141.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  rows = sorted(reader, key=lambda row: row[1], reverse=True)

# Save to CSV
with open('johncena141.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerows(rows)
