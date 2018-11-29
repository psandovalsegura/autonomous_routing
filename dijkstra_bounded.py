#!/usr/bin/python

def get_network_subset(network, o, d):
    network_subset = network.copy()
    u = max(o[1], d[1])
    l = min(o[1], d[1])
    for n in network: 
        if n[1] < l or n[1] > u:
            network_subset.remove_node(n)
    return network_subset


def update_routes_quickest_bounded(netlogo, network, cars):
    import networkx as nx
    for car in cars:
        if car.stopped and car.direction == 'east':
            next_intersection = car.next_intersection.to_tuple()
            destination = car.destination.to_tuple()
            #print next_intersection
            #print destination
            network_subset = get_network_subset(network, next_intersection, destination)
            #print len(network)
            #print len(network_subset)
            route = nx.shortest_path(network_subset, next_intersection, destination, 'time')
            car.push_route_netlogo(netlogo, route, mode = 'remaining')

