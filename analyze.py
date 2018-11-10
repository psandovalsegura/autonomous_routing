#!/usr/bin/python

# analyze the data coming from netlogo
# update the traffic and speed on networkx
# update the attributes of cars
def analyze(data, cars, network):
    from ast import literal_eval
    from car import update_car
    from network import update_network
    #create a dictionary of the cars on links to
    #update the networkx later with it
    network_usage_dict = dict()

    # go through the data coming from netlogo
    for item in data:
        id, xcor, ycor, link_on,\
        speed, direction, on_route_time, dist_travelled,\
        remaining_route_count, travel_time,\
        iteration = item.split("_")

        # check if the car is entered the core network (red intersections)
        try: 
            past_int, next_int = literal_eval(link_on)
        except:
            past_int, next_int = None, None


        # update the car attributes
        cars = update_car(cars, id, xcor, ycor, past_int, next_int, speed, direction,\
                          on_route_time, dist_travelled, remaining_route_count,\
                          travel_time, iteration)
        
        # if the car is not the core network, networkx is not being updated
        if not past_int:
            continue

        # add to the network usage dictioknary as we stream through
        # the data coming from netlogo
        if not link_on in network_usage_dict:
            network_usage_dict[link_on] = []
        car = [c for c in cars if c.id == int(id)][0]
        network_usage_dict[link_on].append(car)
        
        # now update network (link speed and traffic)
        # based on network_usage_dict
        network = update_network(network, network_usage_dict)

    return cars, network

