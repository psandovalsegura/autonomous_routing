#!/usr/bin/python

# code includes tha class of cars

class Intersection:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Car:
    def __init__(self, origin, destination, id):
        self.origin = origin
        self.destination = destination
        self.id = id
        # Manhattan Distance
        self.distance = (destination.x - origin.x) +\
                        abs(destination.y - origin.y)
        # past intersection
        self.intersection = origin
        # initial heading
        self.heading = 'east'
        # initial current speed
        self.speed = 0
        # average speed from the origin
        self.avg_speed = 0

    ## set a random route according to the origin and destination
    def set_route(self, mode = 'random'):
        if mode == 'random':
            from random import shuffle
            directions = ['east'] * (self.destination.x - self.origin.x)
            if self.destination.y - self.origin.y > 0:
                directions += ['north'] * (self.destination.y - self.origin.y)
            else:
                directions += ['south'] * (self.origin.y - self.destination.y)
            shuffle(directions)
            directions.append('east')
        # assign the string representaion of the route or directions
        self.directions = directions

        # order of intersections to go to the destination
        curr_x = self.origin.x
        curr_y = self.origin.y
        route = [Intersection(curr_x, curr_y)]
        for d in self.directions:
            if d == 'east':
                curr_x +=1
            elif d == 'north':
                curr_y += 1
            elif d == 'south':
                curr_y -= 1
            route.append(Intersection(curr_x, curr_y))
        self.route = route
        self.remaining_route = route

    ## get the string representation of the route to pass onto netlogo
    def get_directions_str(self):
        return str(self.directions).replace('\'', '\"').replace(',', '')




# create cars, assigns random routes and finishes up the setup
def create_cars(n, s, netlogo): # takes the number of cars, the grid size, and netlogo object
    from random import randrange
    cars = []
    for i in range(n):
        origin = Intersection(0, randrange(s))
        destination = Intersection(s - 1, randrange(s))
        c = Car(origin, destination, len(cars)) # assign a new id to the new car, incremental
        c.set_route()
        cars.append(c)
        netlogo.command('setup-car-python %d %d %d %s' % (c.id,
                                                          c.origin.y,
                                                          c.destination.y,
                                                          c.get_directions_str()))
    # Finish the setup
    netlogo.command('finish-setup')
    return cars


