#!/usr/bin/python
# This file controls Netlogo from Python


# analyze the data coming from netlogo
# update the traffic and speed on networkx
def analyze(data, network):
    from ast import literal_eval
    for e in network.edges():
        network[e[0]][e[1]]['traffic'] = 0
        network[e[0]][e[1]]['speed'] = []

    for item in data:
        id, link_on, speed = item.split("_")
        if link_on == 'NA':
            continue
        id = int(id); speed = float(speed)
        o, d = literal_eval(link_on)
        network[o][d]['traffic'] += 1
        network[o][d]['speed'].append(speed)
    return network

if __name__ == '__main__':
    import sys
    from netlogo import *
    from car import *
    from network import *
    
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

    # temp
    #x = raw_input()
    #netlogo.kill_workspace()

    from collections import Counter
    average_travel_times = []
    try:
        for i in range(500):
            netlogo.command('go')

            # take the average travel time of all the agents at each point
            average_travel_times.append(netlogo.report('mean [travel_time] of turtles'))

            # extract data form netlogo: {agent_id - link_on - speed}
            data = netlogo.report('[data] of turtles')
            network = analyze(data, network)

            #x = raw_input()
            
    except KeyboardInterrupt:
        pass

    netlogo.kill_workspace()

