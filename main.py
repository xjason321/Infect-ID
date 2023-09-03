import networksim as network
import random
import window


nodes = [] # list of "Node" objects

# CONFIG FOR EASY ACCESS
SIZE = 30
TIME = random.randint(5, 7)
MIN_CONNECTIONS, MAX_CONNECTIONS = random.randint(0, 1), random.randint(3, 4)

# Network creation and infection simulation
network.createNodeNetwork(SIZE, nodes, MIN_CONNECTIONS, MAX_CONNECTIONS)
p_zero = network.runInfectionSimulation(TIME, nodes)
  
window.CreateNetwork(SIZE)