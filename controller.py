#!/usr/bin/python

# This file controls Netlogo from Python


if __name__ == '__main__':
    import pyNetLogo
    import sys
    from random import randrange
    from car import *
    
    GRID_SIZE = 5
    NUM_CARS = 100
    netlogo = pyNetLogo.NetLogoLink(gui=True,
                                    netlogo_home = '/home/alire/app/netlogo-5.3-64/app/',
                                                    #path to Netlogo installation (jar files,
                                                    #note the "/app")
                                    netlogo_version = '5')
                                                      #netlogo version, either '5' or '6'
    netlogo.load_model('/home/alire/mas/project/autonomous_routing/mars.nlogo')
                        #path to the model

    netlogo.command('set grid-size %d' % (GRID_SIZE))
    #netlogo.command('set num-cars %d' % (NUM_CARS))
    netlogo.command('setup')
    
    # create cars
    cars = []
    for i in range(NUM_CARS):
        origin = Intersection(0, randrange(GRID_SIZE))
        destination = Intersection(GRID_SIZE - 1, randrange(GRID_SIZE))
        c = Car(origin, destination)
        c.set_route()
        cars.append(c)
        netlogo.command('setup-car-python %d %d %s' % (c.origin.y,
                                                       c.destination.y,
                                                       c.get_route_str()))

    netlogo.command('finish-setup')

    x = raw_input()
    netlogo.kill_workspace()
    #while netlogo.report('ticks') < 1000:
    #    netlogo.command('go')

