import random as rm
import tkinter as tk
import player_actions as player
import keyboard
from tkinter import Canvas, ttk

def onObjectClick(nodes, root, canvas):
    def inner(event):
        canvas_item = event.widget.find_withtag(tk.CURRENT)
        if canvas_item:
            print(event.x, event.y)
            tags = event.widget.gettags(canvas_item[0])
            for tag in tags:
                if tag.startswith("Node-"):
                    node_id = tag[len("Node-"):]
                    # Now you have the node_id
                                        
                    if keyboard.is_pressed('enter'):
                      print(f'The player is locking in {node_id}')
                      player.lockin(int(node_id), nodes, root, canvas)
                    else:
                      player.sample(int(node_id), nodes, root, canvas)

                    break  # Assuming there's only one "Node-" tag per object

    return inner

def CreateNetwork(nodes, root, canvas):

  running = True

  while running:
    for node in nodes:
      for neighbor in node.connections:   
        canvas.create_line(node.X+15, node.Y+15, neighbor.X+15, neighbor.Y+15, fill="burlywood", dash=(100))
    
    for node in nodes:
      if node.visibleToPlayer:
        color = "tomato" if node.state == 1 else "pale green"
        color = "purple" if node.isPatientZero else color
      else:
        color = "white"

      newNode = canvas.create_oval(node.X, node.Y, \
                                  node.X + 30, node.Y + 30, \
                                  fill=color, outline="white", \
                                  width=2, tags="Node-"+str(node.id))
                        
      canvas.tag_bind("Node-"+str(node.id), '<Button-1>', onObjectClick(nodes, root, canvas))

    canvas.pack()
    root.update()

def update(nodes, root, canvas):
    canvas.delete("all") # reload canvas
    CreateNetwork(nodes, root, canvas)