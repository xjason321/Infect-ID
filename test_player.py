import random
import Node as nn
import csv
import Player
import Graph as graph

csv_path = "a.csv"

player1 = Player.Player(100, 2, 3, 4, 0.1, csv_pathway=csv_path)

player1.load_csv()

lis = player1.nodes

graph.CreateGraphHTML(player1)