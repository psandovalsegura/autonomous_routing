#!/usr/bin/python

def make_temp_route(car):
    o = car.next_intersection
    d = car.destination
    dx = d.x - o.x
    dy = d.y - o.y
    curr_x = o.x
    curr_y = o.y
    r = [(o.x, o.y)]
    for i in range(dx):
        curr_x += 1
        r.append((curr_x, curr_y))
    if dy > 0:
        for i in range(dy):
            curr_y += 1
            r.append((curr_x, curr_y))
    if dy < 0:
        for i in range(abs(dy)):
            curr_y -= 1
            r.append((curr_x, curr_y))
    print r
    return r
    
