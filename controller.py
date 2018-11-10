#!/usr/bin/python
# This file controls Netlogo from Python


# analyze the data coming from netlogo
# update the traffic and speed on networkx
# update the attributes of cars

def analyze(data, network):
    from ast import literal_eval
    # reset the networkx
    for e in network.edges():
        network[e[0]][e[1]]['traffic'] = 0
        network[e[0]][e[1]]['speed'] = []

    # go through the data coming from netlogo
    for item in data:
        id, xcor, ycor, link_on,\
        speed, direction, on_route_time,\
        remaining_route_count, travel_time,\
        iteration = item.split("_")

        at_origin = False
        try: 
            past_int, next_int = literal_eval(link_on)
        except:
            at_origin = True
            past_int, next_int = None, None


        # update the car attributes
        update_car(cars, id, xcor, ycor, past_int, next_int, speed, direction,\
                   on_route_time, remaining_route_count,\
                   travel_time, iteration)

        if at_origin:
            continue

        network[past_int][next_int]['traffic'] += 1
        network[past_int][next_int]['speed'].append(speed)
    return network

if __name__ == '__main__':
    import sys
    from netlogo import fire_up
    from network import create_network
    from car import *
    
    # globals
    GRID_SIZE = 5
    NUM_CARS = 100

    # Fire up the model
    netlogo = fire_up(GRID_SIZE)

    # Create Networkx, representative of netlogo transportaiton network in python
    network = create_network(GRID_SIZE)

    # create cars and assign random routes, and finish the setup
    cars = create_cars(NUM_CARS, GRID_SIZE, netlogo)

    # Run the procedure
    try:
        for i in range(500):
            x = raw_input()
                       
            netlogo.command('go')
            # extract data form netlogo: {agent_id xcor ycor link_on speed direction
            #                             on_route_time remaining_route travel_time iteration}
            data = netlogo.report('[data] of turtles')
            network = analyze(data, network)
        
            if i == 0:
                id = netlogo.report('[id] of one-of turtles with [not hidden?]')
                car = [c for c in cars if c.id == int(id)][0]
                netlogo.command('inspect one-of turtles with [id = %s]' % id)
                netlogo.command('watch one-of turtles with [id = %s]' % id)

            car.show_attributes()


           
    except KeyboardInterrupt:
        pass

    netlogo.kill_workspace()

