import random
import Node as nn
import csv
import Player

csv_path = "a.csv"

player1 = Player.Player(100, 2, 3, 4, 0.1, csv_pathway=csv_path)

player1.load_csv()

lis = player1.nodes

for node in lis:

    print(node.id)
    print(node.name)
    print(node.connections)
    print(node.connectNumbers)
    print("\n\n")
