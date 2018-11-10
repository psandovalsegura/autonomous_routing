#!/usr/bin/python

# analyze the data coming from netlogo
# update the traffic and speed on networkx
# update the attributes of cars
def analyze(data, cars, network):
    from ast import literal_eval
    from car import update_car
    # reset the networkx
    for e in network.edges():
        network[e[0]][e[1]]['traffic'] = 0
        network[e[0]][e[1]]['speed'] = []

    # go through the data coming from netlogo
    for item in data:
        id, xcor, ycor, link_on,\
        speed, direction, on_route_time, dist_travelled,\
        remaining_route_count, travel_time,\
        iteration = item.split("_")

        at_origin = False
        try: 
            past_int, next_int = literal_eval(link_on)
        except:
            at_origin = True
            past_int, next_int = None, None


        # update the car attributes
        cars = update_car(cars, id, xcor, ycor, past_int, next_int, speed, direction,\
                          on_route_time, dist_travelled, remaining_route_count,\
                          travel_time, iteration)

        if at_origin:
            continue

        network[past_int][next_int]['traffic'] += 1
        network[past_int][next_int]['speed'].append(speed)
    return cars, network

