import Player as p
import Graph as graph
import Algorithm as a
import random
import math

from flask import Flask, render_template

def run_ai(ai, player, percentSamples, percentTraced):

  numSamples = round(percentSamples * player.size)
  numTraced = round(percentTraced * numSamples)
  numberToSelect = math.ceil(0.03 * player.size)

  for _ in range(numSamples):
    chosen = ai.ChooseOneToSample(player)
    player.sample(chosen)

  print(f"Sampled {len(player.sampled)} Nodes: {player.sampled}")

  # After, calculate likelihoods
  sorted_indices = ai.getSortedIds()
  # Find spread pattern for most likely
  for Id in sorted_indices[:numTraced]:
    ai.TraceSpreadPattern(player, Id)

  traced = sorted_indices[:numTraced]

  print(f"Traced Spread Patterns For {sorted_indices[:numTraced]}")

  # Compare likelihoods again
  sorted_indices = ai.getSortedIds()

  # Print 5 Top Choices (rightmost is the one it's most confident in)
  print(
      f"Top Choices From AI (least confident to most confident, right being most confident): \n{sorted_indices[-numberToSelect:]}"
  )

  for nodeNumber in sorted_indices[-numberToSelect:]:
    player.nodes[nodeNumber].selectedByAI = "True"

  return sorted_indices, traced


app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index():
  # NEAT GENOME SHIT: (THESE ARE GENERATED)
  negativeEffectBias = 70.16
  positiveBias = 58.123
  positiveEffectBias = 22.98
  similarityWeight = 119.5
  percentSamples = 0
  percentTraced = 0

  # Random pathway -------
  # player = p.Player(
  #     size=random.randint(50, 100),
  #     time=random.randint(1, 3),
  #     min=random.randint(1, 2),
  #     max=random.randint(2, 3),
  #     percent=random.uniform(0.15, 0.25)  # initially given
  # )
  #----------

  # User Uploaded pathway -------
  csv_path = "a.csv"

  player = p.Player(17, 2, 3, 4, 0.1, csv_pathway=csv_path)

  player.load_csv()
  # -------------------


  # FOR GEORGE: Uncomment this and change Algorithm.py to match dictionary
  ai = a.Algorithm(
       size=player.size,

       # NEAT
       negativeEffectBias=negativeEffectBias,
       positiveBias=positiveBias,
       positiveEffectBias=positiveEffectBias,
       similarityWeight=similarityWeight)

  sorted, traced = run_ai(ai, player, percentSamples, percentTraced)
  
  # Start window loop
  nodes, edges = graph.CreateGraphHTML(player, "templates/index.html")

  numPositive, numNegative, numUnknown = 0, 0, 0
  for node in player.nodes.values():
    if node.visibleToPlayer == False:
      numUnknown += 1
    elif node.state == 1: 
      numPositive += 1
    elif node.state == 0:
      numNegative += 1
  
  return render_template('index.html',
                         nodes=nodes,
                         edges=edges,
                         num_nodes=len(player.nodes),
                         num_positive=numPositive,
                         num_negative=numNegative,
                         num_unknown=numUnknown,
                         alloted_time=player.time,
                         min=player.min_connections,
                         max=player.max_connections,
                         num_visible=player.num_visible_to_player)


# if __name__ == "__main__":  # Makes sure this is the main process
#   app.run(  # Starts the site
#       host=
#       '0.0.0.0',  # EStablishes the host, required for repl to detect the site
#       port=random.randint(
#           2000, 9000)  # Randomly select the port the machine hosts on.
#   )
