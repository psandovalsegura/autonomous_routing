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
            # extract data form netlogo: {agent_id xcor ycor link_on speed direction on_route_time
            #                             dist_travelled remaining_route travel_time iteration}
            data = netlogo.report('[data] of turtles')
            cars, network = analyze(data, cars, network)
        
            if i == 0:
                id = netlogo.report('[id] of one-of turtles with [not hidden?]')
                car = [c for c in cars if c.id == int(id)][0]
                netlogo.command('inspect one-of turtles with [id = %s]' % id)
                netlogo.command('watch one-of turtles with [id = %s]' % id)

            car.show_attributes()


           
    except KeyboardInterrupt:
        pass

    netlogo.kill_workspace()

