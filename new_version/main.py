import node_network as node_network
import random
import window
import time
import tkinter as tk
from tkinter import Canvas, ttk
import player_actions

nodes = [] # list of "Node" objects

# CONFIG FOR EASY ACCESS
SIZE = 100
TIME = random.randint(2, 6)
MIN_CONNECTIONS, MAX_CONNECTIONS = random.randint(0, 1), random.randint(2, 3)
NUM_VISIBLE_TO_PLAYER = round(.1 * SIZE) # Replace .1 with percent nodes visible to player

# Network creation and infection simulation
node_network.createNodeNetwork(SIZE, nodes, MIN_CONNECTIONS, MAX_CONNECTIONS)
node_network.runInfectionSimulation(TIME, nodes)

# Make x amount of nodes visible to player.
for i in range(NUM_VISIBLE_TO_PLAYER):
    while True:
        node = random.choice(nodes)

        if node.visibleToPlayer == False:
            node.visibleToPlayer = True
            break

# Set up tkinter canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=620, height=620)
canvas.config(background="gray90")

# Start window loop
window.CreateNetwork(nodes, root, canvas)