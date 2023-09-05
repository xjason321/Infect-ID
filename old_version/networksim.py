import random
import window

global p_zero

class Node():

  def __init__(self, id):
    self.id = id
    self.state = 0  # 1 is infected
    self.connections = []
    self.connectNumbers = []
    
    self.age = random.randint(1, 80)

  def makeConnections(self, nodes, min_connections, max_connections):
    numberConnections = random.randint(min_connections, max_connections)

    for i in range(numberConnections):
      # Mark a new target
      target = random.randint(0, len(nodes) - 1)

      # If not already connected or target is not self
      if nodes[target] not in self.connections and \
      target != self.id and \
      self not in nodes[target].connections:

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
  
  def infectNeighbors(self):
    # Infect all uninfected neighbors
    for neighbor in self.connections:
      # Calculate infection likelihood
      likelihood = neighbor.calculateLikelihood()
      
      if random.randint(0, 1000)/10 <= likelihood:
        neighbor.state = 1


def createNodeNetwork(numberOfNodes, nodes, min_connections, max_connections):
  # Create nodes
  for newNodeId in range(numberOfNodes):
    nodes.append(Node(newNodeId))

  # Make connections
  for node in nodes:
    node.makeConnections(nodes, min_connections, max_connections)

  # print("------ Creating Network -----")

  # # For testing: Print network of nodes
  for i in range(len(nodes)):

    print(f"Node {i}: Connected with {nodes[i].connectNumbers}")
    window.Robbery(nodes[i].connectNumbers)

  print("--------- DONE -----------")

def runInfectionSimulation(numDays, nodes):
  # Determine if it is the first day
  firstDay = True
  for node in nodes:
      if node.state == 1:
        firstDay = False
  
  if firstDay:
    # Select patient zero
    p_zero = random.choice(nodes)
    p_zero.state = 1
    print(f"Patient-Zero is Node #{p_zero.id}\n--------------------------")
  
    # Just to make it easier to read on right
    print("Infected Nodes After Day 0 --------------------")
    print(p_zero.id)

  for day in range(1, numDays + 1):
    print(f"\nInfected Nodes After Day {day} --------------------")

    infectednodes = []

    for node in nodes:
      if node.state == 1:
        infectednodes.append(node)

    for node in infectednodes:
      if node.state == 1:
        node.infectNeighbors()

    # For testing:
    for node in nodes:
      if node.state == 1:
        print(node.id, end=" ")
        window.ReceiveStatus(node.id)
    print("")

    #print("###", infectednodes)
    #window.ReceiveStatus(infectednodes)

  return p_zero
