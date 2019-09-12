#!/usr/bin/python

# opens up the model and initialize
def fire_up(s, gui = True): # takes the size of the grid and GUI
    import pyNetLogo
    import os

    autonomous_routing = "/Users/pedrosandoval/Documents/MASResearch/autonomous_routing/mars.nlogo"
    netlogo_location = "/Volumes/NetLogo-5.3/NetLogo 5.3" 
    
    netlogo = pyNetLogo.NetLogoLink(gui=gui, netlogo_home=netlogo_location, netlogo_version='5')
                                
    netlogo.load_model(autonomous_routing) 

    # path to the model
    # adjusts the grid size
    netlogo.command('set grid-size %d' % (s))
    # setup the grid, origins, and destinations
    netlogo.command('setup')
    return netlogo
