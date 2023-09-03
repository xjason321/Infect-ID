#DO NOT TOUCH THIS CODE IT IS VERY FRAGILE BUT I HAD TO GO I WILL FIX IT OK BYE

import random as rm
import tkinter as tk
from tkinter import Canvas, ttk


root = tk.Tk()

#do not delete
"""
def mainW():
  frm = ttk.Frame(root, padding=100)
  frm.grid()
  
  ttk.Label(frm, text="test", font="Arial 50") \
  .grid(column=0, row=0)
  
  ttk.Button(frm, text="Quit", \
      command=root.destroy).grid(column=0, row=15)
  
  ttk.Label(frm, text="test2").grid(column=50, row=50)
  
  root.mainloop()
"""
#class Node:
  #def __init__(self, cenX, cenY):
    #self.cenX = cenX
    #self.cenY = cenY

  #def DefineNeighbors(self, cenX, cenY, neighborX, neighborY):

#to do: drawing connections between nodes
#have an array of x and y vals
#assign circles to nodes
#calculate slope, draw lines between points
#note all radii = 5
def CreateNetwork(size):
  canvas = tk.Canvas(root, width=200, height=200)
  
  for x in range(0, size):
    # Prevent repeating of nodes
    while True:
      randX = rm.randint(2, 18) * 10
      randY = rm.randint(2, 18) * 10
      
      if randX not in centerXvalues and randY not in centerYvalues:
        break
    
    canvas.create_oval(randX, randY, \
                       randX + 10, randY + 10)

    centerXvalues.append(randX + 5)
    centerYvalues.append(randY + 5)

    print(centerXvalues, centerYvalues)

    #newNode = Node(randX + 5, randY + 5)
    #nodes.append(newNode)

  canvas.pack()
  root.mainloop()

#def DrawLines(i, neighborPos):
  #canvas = tk.Canvas(root, width=200, height=200)
  
  #canvas.create_line((centerXvalues[i], centerYvalues[i]), \
  #(centerXvalues[neighborPos], centerYvalues[neighborPos]))

  #canvas.pack()
  #root.mainloop()

centerXvalues = []
centerYvalues = []
nodes = []
