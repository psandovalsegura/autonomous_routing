#!/usr/bin/python

def create_network(s):
    import networkx as nx
    g = nx.DiGraph()

    for i in range(s):
        for j in range(s):
            g.add_node((i,j))
    for j in range(s):
        for i in range(s):
            g.add_edge((i - 1,j), (i, j), traffic = 0, speed = [])
        g.add_edge((i,j), (i + 1, j), traffic = 0, speed = [])

    for i in range(s):
        for j in range(s - 1):
            g.add_edge((i, j), (i, j + 1), traffic = 0, speed = [])
            g.add_edge((i, j + 1), (i, j), traffic = 0, speed = [])

    return g
    
    

if __name__ == '__main__':
    create_network(5)
