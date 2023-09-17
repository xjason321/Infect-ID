import Player as p
import tkinter as tk
import Window as window
import Algorithm as a

player = p.Player()
nodes = player.nodes
print("-------------------------------------------------")
print(f"Actual Patient Zero: {player.p_zero}")

# Set up tkinter canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=620, height=620)
canvas.config(background="gray90")

"""
THIS IS THE ACTUAL AI PART ---------------------------------------------------
"""
ai = a.Algorithm(len(player.nodes))

# Sample 20 Nodes
for i in range(20):
    chosen = ai.ChooseOneToSample(player)
    player.sample(chosen)

print(f"Sampled {len(player.sampled)} Nodes: {player.sampled}")

# After, calculate likelihoods
sorted_indices = ai.getSortedIds()

# Find spread pattern for most likely
for Id in sorted_indices:
    ai.TraceSpreadPattern(player, Id)

print("Traced Spread Patterns For [All Nodes]")

# Compare likelihoods again
sorted_indices = ai.getSortedIds()

# Print 5 Top Choices (rightmost is the one it's most confident in)
print(f"Top Choices From AI (least confident to most confident, right being most confident): \n{sorted_indices[-5:]}")

"""
THIS IS THE ACTUAL AI PART ---------------------------------------------------
"""


# Start window loop
window.CreateNetwork(root, canvas, player)
