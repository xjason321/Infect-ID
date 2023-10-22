import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

def CreateGraphHTML(player, path):
  G = nx.Graph()

  elements = []

  for i, node in enumerate(player.nodes):

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

    elements.append((i, {"ID": str(node.id),\
                         "Status": status,\
                         "color": color,\
                         "Age": str(node.age),\
                         "Connections": str(node.connectNumbers),\
                         "TimeInfected": str(node.timeInfected) if node.timeInfected else "N/A",\
                         "chosen": node.selectedByAI
                        }))

  G.add_nodes_from(elements)

  for node in player.nodes:
    for connection in node.connectNumbers:
      G.add_edge(node.id, connection)

  nt = Network(notebook=True)
  nt.from_nx(G)

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
  for node in nt.nodes:
      node_str = """Node {ID} - Status: {Status}

                    Age: {Age} y/o
                    Connections: {Connections}
                    Time Infected: {TimeInfected}

                    Chosen By AI: {chosen}
                    """
      node["title"] = node_str.format(**node)

      if node["chosen"] == "True":
        node["size"] = 30

  # nt.show("template.html")  # Save the visualization to an HTML file

  html = nt.generate_html().split("\n")
  
  if len(player.nodes) < 100:
    node_line, edges_line = 90, 91
  else:
    node_line, edges_line = 168, 169

  nodes = html[node_line]
  edges = html[edges_line]
  
  return nodes, edges
