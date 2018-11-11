#!/usr/bin/python

# this creates the core transporation network that is being analyzed
# red intersections are the nodes
def create_network(s):
    import networkx as nx
    g = nx.DiGraph()
    SPEED_LIMIT = 0.5 ## speed limit set in netlogo

    # adding nodes
    for i in range(s):
        for j in range(s):
            g.add_node((i,j))
    
    # adding east-west edges
    for j in range(s):
        for i in range(s - 1):
            g.add_edge((i, j), (i + 1, j), cars= [], traffic = 0, speed = SPEED_LIMIT,
                                                                  time = 1. / SPEED_LIMIT)

    for i in range(s):
        for j in range(s - 1):
            g.add_edge((i, j), (i, j + 1), cars = [], traffic = 0, speed = SPEED_LIMIT,
                                                                   time = 1. / SPEED_LIMIT)
            g.add_edge((i, j + 1), (i, j), cars = [], traffic = 0, speed = SPEED_LIMIT,
                                                                   time = 1. / SPEED_LIMIT)

    return g
    
    
def update_network(network, network_usage_dict):
    from ast import literal_eval
    import numpy as np
    SPEED_LIMIT = 0.5 ## speed limit set in netlogo
    for edge in network.edges():
        # making the dictionary key out of the dge,
        # removing the first and last paranthesis, and the spaces,
        # this is how road_on is brought in from netlogo (a,b),(c,d)
        edge_str = str(edge)[1:-1].replace(" ", "")
        past_int, next_int = edge
        cars_on = []
        mean_speed = SPEED_LIMIT
        if edge_str in network_usage_dict:
            cars_on = network_usage_dict[edge_str]
            mean_speed = np.mean([c.speed for c in cars_on])
        network[past_int][next_int]['cars'] = cars_on
        network[past_int][next_int]['speed'] = mean_speed
        network[past_int][next_int]['traffic'] = len(cars_on)
        network[past_int][next_int]['time'] = 1. / mean_speed
    return network

