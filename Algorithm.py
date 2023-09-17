import Player as p
import copy
import Node as nn
import math, random

# Loop through database
# If a node is negative, lower the chances of its neighbors being p_zero by their age likelihood
# Sample most likely p_zero
# Repeat

# After (.6 * SIZE) times:
# Run simulation on most likely and find infection pattern
# Calculate likelihood of being p_zero

class Algorithm():
    def __init__(self, size):
        self.nodeLikelihoods = [1] * size

    def InitialScan(self, nodes):
        # All negative nodes can't be patient zero, and the chances
        # of their neighbors being patient zero is less.
        for node in nodes:
            if node.state == 0:
                self.nodeLikelihoods[node.id] = 0
                for neighbor in node.connections:
                    self.nodeLikelihoods[neighbor.id] /= 2
            elif node.state == 1:
                self.nodeLikelihoods[node.id] += 0.1
                for neighbor in node.connections:
                    self.nodeLikelihoods[neighbor.id] += 0.1
    
    def ChooseOneToSample(self, nodes):
        # Find most likely after initial scan
        self.InitialScan(nodes)
        mostLikely = max(self.nodeLikelihoods)
        
        # Find most likely nodes and sample them
        likelyNodes = []
        for node in nodes:
            if self.nodeLikelihoods[node.id] == mostLikely:
                likelyNodes.append(node.id)
        
        return random.choice(likelyNodes) 
       
    def FindDifference(list1, list2):
        # Calculate Jaccard similarity
        intersection = len(set(list1).intersection(set(list2)))
        union = len(set(list1).union(set(list2)))
        jaccard_similarity = intersection / union
        
        return jaccard_similarity

    def TraceSpreadPattern(self, Player, target_node):
        new_player = copy.deepcopy(Player)
        
        # Reset infections
        for node in new_player.nodes:
            node.state = 0

        nn.runInfectionSimulation(4, new_player.nodes, selected_p_zero=new_player.nodes[target_node])

        infectionsForNewPlayer = [node.state for node in new_player.nodes]
        infectionsForCurrentPlayer = [node.state for node in Player.nodes]

        difference = math.fabs(Algorithm.FindDifference(infectionsForNewPlayer, infectionsForCurrentPlayer))

        self.nodeLikelihoods[Player.nodes[target_node].id] -= difference
    
    def getSortedIds(self):
        indexed_arr = [(value, index) for index, value in enumerate(self.nodeLikelihoods)]

        # Sort the list of tuples based on values
        sorted_arr = sorted(indexed_arr, key=lambda x: x[0])

        # Extract the sorted indices
        sorted_indices = [index for _, index in sorted_arr]

        return sorted_indices