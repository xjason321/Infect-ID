import random
import Node as nn
import csv

class Player():
    def __init__(self, size, time, min, max, percent, csv_pathway=None):
        self.nodes = {} # dictionary of "Node" objects "
        self.size = size
        self.time = time
        self.min_connections, self.max_connections = min, max
        self.num_visible_to_player = round(percent * self.size) # Replace .1 with percent nodes visible to player
        self.csv = csv_pathway

        # new shit
        self.sampled = []
        self.is_winner = False
        self.is_done = False

        if csv_pathway == None:        
            # Network creation and infection simulation
            nn.createNodeNetwork(self.size, self.nodes, self.min_connections, self.max_connections)
            
            self.p_zero = nn.runInfectionSimulation(self.time, self.nodes)

            print(self.p_zero)
    
            # Make x amount of nodes visible to player.
            for i in range(self.num_visible_to_player):
                while True:
                    node = random.choice(self.nodes)
    
                    if node.visibleToPlayer == False:
                        node.visibleToPlayer = True
                        break

    def load_csv(self):

        Node_data = {}

        with open(self.csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            
            next(reader, None)
                
            for row in reader:
                Id = int(row[0])
                value = row[1:]
                
                Patient_name = value[0]
                
                if value[1] == "Negative":
                    state = 0
                    visible = True
                elif value[1] == "Positive":
                    state = 1
                    visible = True
                else:
                    state = None
                    visible = False

                connections = value[2].split(", ")

                Node_data[Id] = (Patient_name, state, connections, visible)

        for node in Node_data.keys():
            ns = nn.Node(node)
            self.nodes[node] = ns
        
        for node in self.nodes.values():
            Id = node.id
            Patient_name = Node_data[Id][0]
            state = Node_data[Id][1]

            connections = []

            for id in Node_data[Id][2]:
                connections.append(self.nodes[int(id)])
            
            node.state = state
            node.name = Patient_name
            node.visibleToPlayer = Node_data[Id][3]
            
            for target_node in connections:
                node.connectNumbers.append(int(target_node.id))
                node.connections.append(self.nodes[target_node.id])

        print(self.nodes)
    
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
