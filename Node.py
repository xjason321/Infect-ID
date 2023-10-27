import random


class Node():

  def __init__(self, id, centerValues=0):
    self.id = id
    self.state = 0  # 1 is infected
    self.connections = []
    self.connectNumbers = []

    self.visibleToPlayer = False
    self.isPatientZero = False
    self.timeInfected = None
    self.selectedByAI = "False"

    self.X = 0
    self.Y = 0
    
    self.age = random.randint(1, 80)

  def add_connections(self, node, ID):

    self.connections.append(node)
    self.connectNumbers.append(ID)

  def makeConnections(self, nodes, min_connections, max_connections):
    numberConnections = min_connections

    for i in range(numberConnections):
      while True:
        target = random.randint(0, len(nodes) - 1)
        # If not already connected or target is not self
        if nodes[target] not in self.connections and target != self.id:
          break
      
      self.connections.append(nodes[target])
      self.connectNumbers.append(nodes[target].id)

      nodes[target].connections.append(self)
      nodes[target].connectNumbers.append(self.id)

  def calculateLikelihood(self, enableAlwaysInfection=False):
    if 0 <= self.age <= 17:
      likelihood = 45.5
    elif 18 <= self.age <= 49:
      likelihood = 64.9
    elif 50 <= self.age <= 64:
      likelihood = 53.6
    elif self.age >= 65:
      likelihood = 42.36
    else:
      likelihood = 54.6

    return 100 if enableAlwaysInfection else likelihood
  
  def infectNeighbors(self, time):
    # Infect all uninfected neighbors
    for neighbor in self.connections:
      if neighbor.state == 0:
        # Calculate infection likelihood
        likelihood = neighbor.calculateLikelihood()
        
        if random.randint(0, 1000)/10 <= likelihood:
          neighbor.state = 1
          neighbor.timeInfected = time
        
def createNodeNetwork(numberOfNodes, nodes, min_connections, max_connections):
  # Initialize center values:
  centerValues = []

  # for x in [i for i in range(30, 180, 30)]:
  #   for y in [i for i in range(30, 180, 30)]:
  #     centerValues.append
  
  # Create nodes
  for newNodeId in range(numberOfNodes):
    nodes.append(Node(newNodeId, centerValues))
    centerValues.append((nodes[newNodeId].X, nodes[newNodeId].Y))

  # Make connections
  for node in nodes:
    node.makeConnections(nodes, min_connections, max_connections)

def runInfectionSimulation(numDays, nodes, selected_p_zero=None):
  # Select patient zero
  p_zero = selected_p_zero if selected_p_zero else random.choice(nodes)
  p_zero.state = 1
  p_zero.isPatientZero = True
  p_zero.timeInfected = 0
  # print(f"Patient-Zero is Node #{p_zero.id}, X:{p_zero.X}, Y:{p_zero.Y}\n--------------------------")

  # Just to make it easier to read on right
  # print("Infected Nodes After Day 0 --------------------")
  # print(p_zero.id)

  for day in range(1, numDays + 1):
    # print(f"\nInfected Nodes --------------------")

    infectednodes = []

    for node in nodes:
      if node.state == 1:
        infectednodes.append(node)

    for node in infectednodes:
      if node.state == 1:
        node.infectNeighbors(day)

  return p_zero.id
