#!/usr/bin/python

# code includes tha class of cars

class Intersection:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Car:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

    def set_route(self, mode = 'random'):
        if mode == 'random':
            from random import shuffle
            r = ['east'] * (self.destination.x - self.origin.x)
            if self.destination.y - self.origin.y > 0:
                r += ['north'] * (self.destination.y - self.origin.y)
            else:
                r += ['south'] * (self.origin.y - self.destination.y)
            shuffle(r)
            r.append('east')
        self.route = r

    def get_route_str(self):
        return str(self.route).replace('\'', '\"').replace(',', '')





