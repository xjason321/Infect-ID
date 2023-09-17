import random
import Node as nn

class Player():
    def __init__(self):
        self.nodes = [] # list of "Node" objects
        self.size = 120
        self.time = 4
        self.min_connections, self.max_connections = 1, 2
        self.num_visible_to_player = round(0.3 * self.size) # Replace .1 with percent nodes visible to player
        
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

