import random
import Node as nn
import csv

class Player():
    def __init__(self, size, time, min, max, percent, csv_pathway=None):
        self.nodes = [] # list of "Node" objects "
        self.size = size
        self.time = time
        self.min_connections, self.max_connections = min, max
        self.num_visible_to_player = round(percent * self.size) # Replace .1 with percent nodes visible to player
        self.csv = csv_pathway

        # new shit
        self.sampled = []
        self.is_winner = False
        self.is_done = False

        # Network creation and infection simulation
        nn.createNodeNetwork(self.size, self.nodes, self.min_connections, self.max_connections)
        
        self.p_zero = nn.runInfectionSimulation(self.time, self.nodes)

        # Make x amount of nodes visible to player.
        for i in range(self.num_visible_to_player):
            while True:
                node = random.choice(self.nodes)

                if node.visibleToPlayer == False:
                    node.visibleToPlayer = True
                    break

    def load_csv(self):

        temp_nodes = []
        Node_data = {}

        with open(self.csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            
            next(reader, None)
                
            for row in reader:
                Id = row[0]
                value = row[1:]
                Patient_name = value[0]
                state = value[1]
                connections = value[2]

                Node_data[Id] = (Patient_name, state, connections)

        for node in Node_data.keys():
            ns = nn.Node(node)
            temp_nodes.append(ns) #node -> ID

        for node in temp_nodes:
                
            Id = node.id
            Patient_name = Node_data[Id][0]
            state = Node_data[Id][1]
            connections = Node_data[Id][2]

            node.state = state
            node.name = Patient_name
            for i in connections.split(","):
                node.connectNumbers.append(i)
                node.connections.append(temp_nodes[int(i)-1])

        self.nodes = temp_nodes
        


    # All of this is taken from player_actions.py
    def sample(self, id_to_sample):
        if id_to_sample in self.sampled:
            return 0
        
        self.nodes[id_to_sample].visibleToPlayer = True
        self.sampled.append(id_to_sample)
        
        return id_to_sample, self.nodes[id_to_sample].state

    # All of this is taken from player_actions.py
    def lockin(self, prediction_id):
        if self.is_done:
            return 0
        
        for node in self.nodes:
            node.visibleToPlayer = True
        
        if self.nodes[prediction_id].isPatientZero:
            print(f"Correctly selected patient zero! It is {prediction_id}!")
            self.is_winner = True
        else:
            print("The user guess is wrong.")
            self.is_winner = False

        self.is_done = True
