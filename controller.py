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

if __name__ == '__main__':
    import pyNetLogo
    import sys
    from random import randrange
    from car import *
    
    # globals
    GRID_SIZE = 5
    NUM_CARS = 100

    # Fire up the model
    netlogo = fire_up(GRID_SIZE)

    # create cars and assign random routes, and finish the setup
    cars = create_cars(NUM_CARS)
    
    # Run the procedure

    # temp
    x = raw_input()
    netlogo.kill_workspace()
    
    try:
        for i in range(1000):
            netlogo.command('go')
    except KeyboardInterrupt:
        pass

    netlogo.kill_workspace()

