#!/usr/bin/python

# code includes tha class of cars

class Intersection:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return 'Intersection (%d, %d)' % (self.x, self.y)

    def __str__(self):
        return 'Intersection (%d, %d)' % (self.x, self.y)

class Car:
    def __init__(self, origin, destination, id):
        self.origin = origin  # the red intersections to the left
        self.destination = destination  # the red intersection to the right
        self.id = id
        # Manhattan Distance
        self.distance = (destination.x - origin.x) +\
                        abs(destination.y - origin.y)
        # past intersection
        self.intersection = origin
        # next intersections
        self.next_intersection = origin
        # the road agent is on
        self.road_on = None
        # on_route_time
        self.on_route_time = 0
        # distance travelled
        self.dist_travelled = 0
        # travel_time
        self.travel_time = 0
        # initial heading
        self.direction = 'east'
        # initial current speed
        self.speed = 0
        # average speed from the origin
        self.avg_speed = None
        # the location in netlogo world, will be updated immediately
        # after the start of the model
        self.location = (-1, -1)
        # if the car has stopped behind the stop sign or not
        self.stopped = False
        # How many times the agents has travelled between origin and destination
        self.iteration = 0

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
        # assign the string representaion of the route or directions
        self.directions = directions
        self.remaining_directions = directions
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
        # route gores from the red intersection on the left,
        # to the ACTUAL destination on the right
        self.remaining_route = route

    ## get the string representation of the route to pass onto netlogo
    def get_directions_str(self):
        return str(self.directions).replace('\'', '\"').replace(',', '')

    def route_to_direction(self, route):
        directions = []
        for ind, prev_int in enumerate(route[:-1]):
            next_int = route[ind + 1]
            delta_x = next_int[0] - prev_int[0]
            if delta_x == 1:
                directions.append('east')
                continue
            delta_y = next_int[1] - prev_int[1]
            if delta_y == 1:
                directions.append('north')
                continue
            elif delta_y == -1:
                directions.append('south')
                continue
            else:
                directions.append('none')
        return directions


    def push_route_netlogo(self, netlogo, new_route, mode = 'remaining'): # 'original' 'remaining' 'both'
        new_directions = self.route_to_direction(new_route)
        new_directions_str = str(new_directions).replace('\'', '\"').replace(",", "")
        if mode == 'remaining':
            self.remaining_route = [Intersection(*xy) for xy in new_route]
            self.remaining_directions = new_directions
            netlogo.command('ask turtle %d [update_remaining_route %s]' % (self.id, new_directions_str))
        elif mode == 'original':
            self.route = [Intersection(*xy) for xy in new_route]
            self.directions = new_directions
            netlogo.command('ask turtle %d [update_original_route %s]' % (self.id, new_directions_str))

        # TODO: Fails under specific circumstances
        elif mode == 'both':
            self.route = [Intersection(*xy) for xy in new_route]
            self.directions = new_directions
            self.remaining_route = [Intersection(*xy) for xy in new_route[-len(self.remaining_route):]]
            self.remaining_directions = new_directions[-len(self.remaining_route):]
            netlogo.command('ask turtle %d [update_original_route %s]' % (self.id, new_directions_str))
            netlogo.command('ask turtle %d [update_remaining_route %s]' %\
                            (self.id, str(new_directions[-len(self.remaining_route):]).\
                            replace('\'', '\"').replace(",", "")))
        else:
            print('Invalid Mode!')

    def show_attributes(self):
        from pprint import pprint
        pprint(self.__dict__)



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

# update the car attributes with the ones came from NetLogo
def update_car(cars, id, xcor, ycor, stopped, past_int, next_int, speed, direction,\
               on_route_time, dist_travelled, drop_first_dir,\
               travel_time, iteration):
    id = int(id)
    car = [c for c in cars if c.id == id][0]
    car.speed = float(speed)
    car.location = (float(xcor), float(ycor))
    car.stopped = stopped == 'true'
    car.iteration = int(iteration)
    if car.iteration > 0:
        car.travel_time = int(travel_time)
    else:
        car.travel_time = None
    car.direction = direction
    if drop_first_dir == 'true':
        car.remaining_route = car.remaining_route[1:]
        car.remaining_directions = car.remaining_directions[1:]
    if float(dist_travelled) < 0:
        car.dist_travelled = 0
        car.on_route_time = 0
    else:
        car.dist_travelled = float(dist_travelled)
        car.on_route_time = int(on_route_time)
        if car.on_route_time > 0:
            car.avg_speed = car.dist_travelled / car.on_route_time
    if past_int:
        car.intersection = Intersection(*past_int)
        car.next_intersection = Intersection(*next_int)
        car.road_on = (Intersection(*past_int), Intersection(*next_int))
    else:
        car.intersection = None
        car.next_intersection = car.origin
        car.road_on = None

    return cars
