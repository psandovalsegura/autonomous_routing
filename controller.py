#!/usr/bin/python

# This file controls Netlogo from Python


import pyNetLogo

netlogo = pyNetLogo.NetLogoLink(gui=True,
                                netlogo_home = '/home/alire/app/netlogo-5.3-64/app/',   #path to Netlogo installation (jar files, note the "/app")
                                netlogo_version = '5')                                  #netlogo version, either '5' or '6'
netlogo.load_model('/home/alire/mas/project/autonomous_routing/mars.nlogo')             #path to the model

netlogo.command('setup')

while netlogo.report('ticks') < 1000:
    netlogo.command('go')

