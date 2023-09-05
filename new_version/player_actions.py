import window

def sample(node_id, nodes, root, canvas):
    nodes[node_id].visibleToPlayer = True
    
    window.update(nodes, root, canvas)

    return node_id, nodes[node_id].state


def lockin(prediction_id, nodes, root, canvas):
    for node in nodes:
        node.visibleToPlayer = True
    
    if nodes[prediction_id].isPatientZero:
        print(f"Correctly selected patient zero! It is {prediction_id}!")
    else:
        print("The user guess is wrong.")

    window.update(nodes, root, canvas)