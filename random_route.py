#!/usr/bin/python

def update_random(netlogo, network, cars):
    import networkx as nx
    for car in cars:
        if car.stopped and car.next_intersection.to_tuple() == car.origin.to_tuple():
            car.set_route(mode = 'random')
            route = [intersection.to_tuple() for intersection in car.route]
            car.push_route_netlogo(netlogo, route, mode = 'remaining')

