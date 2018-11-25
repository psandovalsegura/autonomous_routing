#!/usr/bin/python

# opens up the model and initialize
def fire_up(s, gui = True): # takes the size of the grid and GUI
    import pyNetLogo
    import os
    #this finds the location of the project folder and your netlogo folder so we can both work on it, I kept the old code in case this doesnt work for you
    os.system("find /home -type d -name 'autonomous_routing' > find_project_folder.txt")
    os.system("find /home -type d -name 'netlogo-5.3-64' > find_netlogo_folder.txt")
    with open("find_project_folder.txt") as f:
        for line in f:
            autonomous_routing = line.strip() + "/mars.nlogo"
    with open("find_netlogo_folder.txt") as f:
        for line in f:
            netlogo_location = line.strip() + "/app/"
    os.system("rm find_project_folder.txt")
    os.system("rm find_netlogo_folder.txt")
    netlogo = pyNetLogo.NetLogoLink(gui=gui, netlogo_home = netlogo_location, netlogo_version = '5')
                                #path to Netlogo installation (jar files, note the "/app")

                                #netlogo version, either '5' or '6'
    netlogo.load_model(autonomous_routing) #path to the model
    #path to the model
    # adjusts the grid size
    netlogo.command('set grid-size %d' % (s))
    # setup the grid, origins, and destinations
    netlogo.command('setup')
    return netlogo
