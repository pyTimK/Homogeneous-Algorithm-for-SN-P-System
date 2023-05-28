from src.classes.snp_system import SnpSystem
import networkx as nx

def auto_layout(snp_system: SnpSystem):
    graph = nx.Graph()
    nx.spring_layout

    # Add all nodes to networkx graph
    for neuron in snp_system.neurons:
        graph.add_node(neuron.id)
    
    # Add all edges to networkx graph
    for neuron in snp_system.neurons:
        for neuron2Id in neuron.out:
            graph.add_edge(neuron.id, neuron2Id)

    # Get all neurons with no receiving edges (starting neurons)
    neurons_with_no_receiving_edges = {neuron.id for neuron in snp_system.neurons}
    for neuron in snp_system.neurons:
        for neuron2Id in neuron.out:
            if neuron2Id in neurons_with_no_receiving_edges:
                neurons_with_no_receiving_edges.remove(neuron2Id)

    # Uses Fruchterman Reingold technique from networkx library to layout the graph
    pos = nx.fruchterman_reingold_layout(
        graph,
        scale=10.8696 * len(snp_system.neurons) + 391.304, 
        center=[250,250],
    )

    # Finally sets the updated position to the neuron objects
    for neuron in snp_system.neurons:
        neuron.position.x = pos[neuron.id][0]
        neuron.position.y = pos[neuron.id][1]
