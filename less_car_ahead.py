#!/usr/bin/python
def update_routes_less_car_ahead(netlogo, network, cars):
    from random import choice
    import numpy as np
    for car in cars:
        if car.stopped:
            if car.next_intersection.to_tuple() == car.destination.to_tuple():
                continue
            next_intersection = car.next_intersection.to_tuple()
            possible_nodes = []
            delta_y = car.destination.y - car.next_intersection.y
            delta_x = car.destination.x - car.next_intersection.x
            if delta_x > 0:
                node_right = (next_intersection[0] + 1, next_intersection[1])
                possible_nodes.append(node_right)
            if delta_y > 0:
                node_up = (next_intersection[0], next_intersection[1] + 1)
                possible_nodes.append(node_up)
            if delta_y < 0:
                node_down = (next_intersection[0], next_intersection[1] - 1)
                possible_nodes.append(node_down)
            
            if len(possible_nodes) < 2:
                route = [next_intersection, possible_nodes[0]]
            else:
                t0 = network[next_intersection][possible_nodes[0]]
                t1 = network[next_intersection][possible_nodes[1]]
                if t0 < t1:
                    route = [next_intersection, possible_nodes[0]]
                elif t1 < t0:
                    route = [next_intersection, possible_nodes[1]]
                else:    
                    route = [next_intersection, choice(possible_nodes)]

            car.push_route_netlogo(netlogo, route, mode = 'remaining')
