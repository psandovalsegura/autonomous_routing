#!/usr/bin/python

def create_network(s):
    import networkx as nx
    g = nx.DiGraph()
    SPEED_LIMIT = 0.5 ## speed limit set in netlogo

    for i in range(s):
        for j in range(s):
            g.add_node((i,j))
    for j in range(s):
        for i in range(s):
            g.add_edge((i - 1,j), (i, j), cars= [], traffic = 0, speed = SPEED_LIMIT)
        g.add_edge((i,j), (i + 1, j), cars = [], traffic = 0, speed = SPEED_LIMIT)

    for i in range(s):
        for j in range(s - 1):
            g.add_edge((i, j), (i, j + 1), cars = [], traffic = 0, speed = SPEED_LIMIT)
            g.add_edge((i, j + 1), (i, j), cars = [], traffic = 0, speed = SPEED_LIMIT)

    return g
    
    

