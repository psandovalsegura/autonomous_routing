#!/usr/bin/python
# This file controls Netlogo from Python

if __name__ == '__main__':
    import sys
    from time import time
    import numpy as np
    from netlogo import fire_up
    from network import create_network
    from analyze import analyze
    from car import *
    from test import make_temp_route

    from less_car_ahead import update_routes_less_car_ahead
    from dijkstra import update_routes_quickest
    from random_route import update_random
    from decmcts import update_routes_decmcts

    start_time = time()

    # globals
    GRID_SIZE = 5
    NUM_CARS = 20
    SIMULATION_HORIZON = 3000 # in ticks

    # the first argument is the algorithm: "random" "dijkstra" for now
    alg = sys.argv[1]
    if not alg in ['random', 'dijkstra', 'lessCarAhead', 'dynamicRandom', 'decmcts']:
        print('Invalid Option!')
        sys.exit()

    # Fire up the model
    netlogo = fire_up(GRID_SIZE, False)

    # Create Networkx, representative of netlogo transportaiton network in python
    network = create_network(GRID_SIZE)

    # create cars and assign random routes, and finish the setup
    cars = create_cars(NUM_CARS, GRID_SIZE, netlogo)

    # initialize some critical measurements (indicators of mobility)
    mean_travel_times = []
    average_mean_speed_so_far = []

    # Run the procedure
    try:
        for i in range(SIMULATION_HORIZON):
            if i % 500 == 0:
                print(i)
            # uncomment to debug
            #x = raw_input()

            # extract data form netlogo: {agent_id xcor ycor link_on speed direction on_route_time
            #                             dist_travelled remaining_route travel_time iteration}
            data = netlogo.report('[data] of turtles')
            # update cars and networkx
            cars, network = analyze(data, cars, network)

            '''
            YOUR CODE GOES HERE
            UPDATE ROUTES BASED ON
            NETWORK AND CARS
            '''

            if alg == 'dijkstra':
                # SIMPLE DIJKSTRA UPDATE AT EACH INTERSECTION
                update_routes_quickest(netlogo, network, cars)
            if alg == 'lessCarAhead':
                # Turn on the immediate road with higher speed
                update_routes_less_car_ahead(netlogo, network, cars)
            if alg == 'dynamicRandom':
                # each agent takes a new random route at each iteration
                update_random(netlogo, network, cars)
            if alg == 'decmcts':
                update_routes_decmcts(netlogo, cars, GRID_SIZE)

            # monitor average travel times
            mean_travel_times.append(np.mean([c.travel_time for c in cars if c.travel_time]))
            average_mean_speed_so_far.append(np.mean([c.avg_speed for c in cars if c.avg_speed]))




            # advance simulation one step
            netlogo.command('go')

            '''
            if i == 0:
                id = netlogo.report('[id] of one-of turtles with [not hidden?]')
                insp_car = [c for c in cars if c.id == int(id)][0]
                netlogo.command('inspect one-of turtles with [id = %s]' % id)
                netlogo.command('watch one-of turtles with [id = %s]' % id)
                INSPECT = id
                #print INSPECT
            #print [(a.x, a.y) for a in insp_car.remaining_route]
            print insp_car.remaining_directions
            #print [(a.x, a.y) for a in insp_car.route]
            #print insp_car.directions
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

            # uncommend to debug routes updates
            '''
            if x != "":
                mode = 'both' # remaining or original
                car.push_route_netlogo(netlogo, make_temp_route(car), mode = mode)

            if i == 0:
                id = netlogo.report('[id] of one-of turtles with [not hidden?]')
                car = [c for c in cars if c.id == int(id)][0]
                netlogo.command('inspect one-of turtles with [id = %s]' % id)
                netlogo.command('watch one-of turtles with [id = %s]' % id)
            car.show_attributes()
            '''
    # stop simulation at any point with Cntrl+C
    except KeyboardInterrupt:
        pass

    # end session
    t = int(time())
    np.save('results/mean_traveltime_%s_%d.npy' % (alg, t), mean_travel_times)
    np.save('results/mean_speed_%s_%d.npy' % (alg, t), average_mean_speed_so_far)
    past_time = (time() - start_time) / 60.
    print('Elapsed_time: %.1f' % past_time)
    netlogo.kill_workspace()
