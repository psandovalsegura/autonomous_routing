#!/usr/bin/python

# opens up the model and initialize
def fire_up(s, gui = True): # takes the size of the grid and GUI
    import pyNetLogo
    netlogo = pyNetLogo.NetLogoLink(gui=gui,
                                    netlogo_home = '/home/alire/app/netlogo-5.3-64/app/',
                                    # path to Netlogo installation jar files,
                                    # note the "/app"
                                    netlogo_version = '5')
                                    #netlogo version, either '5' or '6'
    netlogo.load_model('/home/alire/mas/project/autonomous_routing/mars.nlogo')
    #path to the model
    # adjusts the grid size
    netlogo.command('set grid-size %d' % (s))
    # setup the grid, origins, and destinations
    netlogo.command('setup')
    return netlogo

