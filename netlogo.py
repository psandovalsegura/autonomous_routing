#!/usr/bin/python

# opens up the model and initialize
def fire_up(s, gui = True): # takes the size of the grid and GUI
    import pyNetLogo
    import os

    autonomous_routing = "/Users/pedrosandoval/Documents/MASResearch/autonomous_routing/mars.nlogo" #path to the model
    netlogo_location = "/Volumes/NetLogo-5.3/NetLogo 5.3" #obtain from https://ccl.northwestern.edu/netlogo/5.3.0/

    # path to Netlogo installation (jar files, note the "/app")
    # netlogo version, either '5' or '6'
    os.chdir(netlogo_location)
    netlogo = pyNetLogo.NetLogoLink(gui=gui, netlogo_home=netlogo_location, netlogo_version='5')
                                
    netlogo.load_model(autonomous_routing) 

    # path to the model
    # adjusts the grid size
    netlogo.command('set grid-size %d' % (s))
    # setup the grid, origins, and destinations
    netlogo.command('setup')
    return netlogo
