from src.classes.snp_system import SnpSystem
import networkx as nx

def auto_layout(snp_system: SnpSystem):
    graph = nx.Graph()
    nx.spring_layout

    for neuron in snp_system.neurons:
        graph.add_node(neuron.id)
    
    for neuron in snp_system.neurons:
        for neuron2Id in neuron.out:
            graph.add_edge(neuron.id, neuron2Id)
    
    pos = nx.spring_layout(graph, scale=550, center=[250,250])

    for neuron in snp_system.neurons:
        neuron.position.x = pos[neuron.id][0]
        neuron.position.y = pos[neuron.id][1]

    print(pos)