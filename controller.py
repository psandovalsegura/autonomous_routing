#!/usr/bin/python
# This file controls Netlogo from Python


# create cars, assigns random routes and finishes up the setup
def create_cars(n): # takes the number of cars
    cars = []
    for i in range(n):
        origin = Intersection(0, randrange(GRID_SIZE))
        destination = Intersection(GRID_SIZE - 1, randrange(GRID_SIZE))
        c = Car(origin, destination, len(cars))
        c.set_route()
        cars.append(c)
        netlogo.command('setup-car-python %d %d %d %s' % (c.id,
                                                          c.origin.y,
                                                          c.destination.y,
                                                          c.get_route_str()))
    # Finish the setup
    netlogo.command('finish-setup')
    return cars

# opens up the model and initialize
def fire_up(s): # takes the size of the grid
    netlogo = pyNetLogo.NetLogoLink(gui=True,
                                    netlogo_home = '/home/alire/app/netlogo-5.3-64/app/',
                                                    #path to Netlogo installation (jar files,
                                                    #note the "/app")
                                    netlogo_version = '5')
                                                      #netlogo version, either '5' or '6'
    netlogo.load_model('/home/alire/mas/project/autonomous_routing/mars.nlogo')
                        #path to the model
    
    # adjusts the grid size
    netlogo.command('set grid-size %d' % (s))

    # setup the grid, origins, and destinations
    netlogo.command('setup')
    return netlogo

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
    import pyNetLogo
    import sys
    from random import randrange
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
    cars = create_cars(NUM_CARS)
    
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

