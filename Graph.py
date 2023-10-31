import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

def CreateGraphHTML(player, path=None):
  G = nx.Graph()

  elements = []

  for i, id in enumerate(player.nodes.keys()):

    node = player.nodes[id]
    
    if node.visibleToPlayer:
      if node.state == 1 and node.isPatientZero:
        status = "Infected"
        color = "purple"
      elif node.state == 1:
        status = "Infected"
        color = "red"
      else:
        status = "Not Infected"
        color = "green"
    else:
      status = "Unknown"
      color = "gray"

    
    elements.append((i, {"ID": str(id),\
                         "Status": status,\
                         "color": color,\
                         "Age": str(node.age),\
                         "Connections": str(node.connectNumbers),\
                         "TimeInfected": str(node.timeInfected) if node.timeInfected else "N/A",\
                         "chosen": node.selectedByAI
                        }))


  G.add_nodes_from(elements)

  #--Bug-- (fixed by Jason 10/28)
  for node in player.nodes.values():
    for connection in node.connections:
      G.add_edge(node.id, connection.id)
  #...
  
  # Create a mapping between NetworkX node IDs and their positions in the elements list
  node_id_to_position = {str(node[1]["ID"]): i for i, node in enumerate(elements)}

  # Create a new Network object
  nt = Network(notebook=True)

  # Add nodes and edges directly from your NetworkX graph
  for node in G.nodes:
      # Get the corresponding position in the elements list based on the node's ID
      position = node_id_to_position.get(str(node), None)

      if position is not None:
          nt.add_node(node, **elements[position][1])  # Add node with attributes

  for edge in G.edges:
      nt.add_edge(edge[0], edge[1])

  nt.width = "70%"

  nt.set_options("""
      var options = {
        "physics": {
          "forceAtlas2Based": {
            "springLength": 100
          },
          "minVelocity": 0.75,
          "solver": "forceAtlas2Based"
        }
      }
      """)

  # Add node information to be displayed on hover
  for i, node in enumerate(nt.nodes):
      n = player.nodes[int(node['label'])]
      id_ = n.id
    
      if n.visibleToPlayer:
        state_ = "Positive" if n.state == 1 else "Negative"
      else:
        state_ = "Unknown"
        
      age_ = n.age
      connections_ = n.connectNumbers
      isPatientZero = n.isPatientZero
      timeInfected_ = n.timeInfected
      selectedbyAI_ = n.selectedByAI
      node["title"] = f"""Node: {id_} - Status: {state_}

                    Age: {age_} y/o
                    Connections: {connections_}
                    Time Infected: {timeInfected_}

                    Chosen By AI: {selectedbyAI_}
                    """

      if selectedbyAI_ == "True":
        node["size"] = 40

  # nt.show("template.html")  # Save the visualization to an HTML file

  html = nt.generate_html().split("\n")
  
  if len(player.nodes) < 100:
    node_line, edges_line = 90, 91
  else:
    node_line, edges_line = 168, 169

  nodes = html[node_line]
  edges = html[edges_line]
  
  return nodes, edges
