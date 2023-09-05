#LETS GOOOO
import random as rm
import tkinter as tk
from tkinter import Canvas, ttk
import networksim

centerXvalues = []
centerYvalues = []
nodeNeighbors = []

nodeValues = []
nodeUI = [] #not using rn
infectedNodes = []

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

#to do: drawing connections between nodes
#have an array of x and y vals
#assign circles to nodes
#calculate slope, draw lines between points
#note all radii = 5
class Node():

  def __init__(self, id, cenX, cenY, neighbors):
    self.id = id
    self.cenX = cenX
    self.cenY = cenY
    self.state = 0  # 1 is infected
    self.neighbors = neighbors

def Robbery(connections):
  nodeNeighbors.append(connections)

def CreateNodes(size):
  for x in range(0, size):
    # Prevent repeating of nodes
    while True:
      randX = rm.randint(2, 18) * 10
      randY = rm.randint(2, 18) * 10
      
      if randX not in centerXvalues and randY not in centerYvalues:
        break

    centerXvalues.append(randX + 5)
    centerYvalues.append(randY + 5)

def ReceiveStatus(node):
  infectedNodes.append(node)
  #infectedNodes = infectednodes
  #print(infectedNodes)

def InitNodes(size):
  for i in range(0, size):
    obj = Node(i, centerXvalues[i], centerYvalues[i], nodeNeighbors[i])
    nodeValues.append(obj)

def CreateNetwork(size):
  canvas = tk.Canvas(root, width=200, height=200)
  
  for i in range(0, size):
    temp = nodeValues[i]

    if temp.id not in infectedNodes:
      obj = canvas.create_oval(temp.cenX - 5., temp.cenY - 5, temp.cenX + 5, temp.cenY + 5)
      nodeUI.append(obj)
    else:
      obj = canvas.create_oval(temp.cenX - 5., temp.cenY - 5, temp.cenX + 5, temp.cenY + 5, fill="red")
      nodeUI.append(obj)

  for i in range(0, size):
    thisNeighbors = nodeNeighbors[i]

    for j in thisNeighbors:
      canvas.create_line((centerXvalues[i], centerYvalues[i]), \
                         (centerXvalues[j], centerYvalues[j]))

  canvas.pack()
  root.mainloop()
