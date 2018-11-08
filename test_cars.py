#!/usr/bin/python

from car import *

O = Intersection(0,10)
D = Intersection(5, 12)

c1 = Car(O, D)

c1.set_route(mode = 'random')

print c1.route
print c1.get_route_str()
