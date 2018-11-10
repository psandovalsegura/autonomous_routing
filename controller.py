#!/usr/bin/python
# This file controls Netlogo from Python


if __name__ == '__main__':
    import sys
    from netlogo import fire_up
    from network import create_network
    from analyze import analyze
    from car import *
    
    # globals
    GRID_SIZE = 5
    NUM_CARS = 100
    SIMULATION_HORIZON = 500 # in ticks

    # Fire up the model
    netlogo = fire_up(GRID_SIZE)

    # Create Networkx, representative of netlogo transportaiton network in python
    network = create_network(GRID_SIZE)

    # create cars and assign random routes, and finish the setup
    cars = create_cars(NUM_CARS, GRID_SIZE, netlogo)

    # Run the procedure
    from random import choice
    try:
        for i in range(SIMULATION_HORIZON):
            # uncomment to debug
            #x = raw_input()

            # advance simulation one step                       
            netlogo.command('go')
            # extract data form netlogo: {agent_id xcor ycor link_on speed direction on_route_time
            #                             dist_travelled remaining_route travel_time iteration}
            data = netlogo.report('[data] of turtles')
            # update cars and networkx
            cars, network = analyze(data, cars, network)
        
            '''
            YOUR CODE GOES HERE
            '''



            # uncommend to debug cars
            '''
            if i == 0:
                id = netlogo.report('[id] of one-of turtles with [not hidden?]')
                car = [c for c in cars if c.id == int(id)][0]
                netlogo.command('inspect one-of turtles with [id = %s]' % id)
                netlogo.command('watch one-of turtles with [id = %s]' % id)
            car.show_attributes()
            '''
            # uncomment to debug networkx
            '''
            if i == 0:
                edge = choice(network.edges())
            print edge, network[edge[0]][edge[1]]
            '''
           
    # stop simulation at any point with Cntrl+C
    except KeyboardInterrupt:
        pass

    netlogo.kill_workspace()

