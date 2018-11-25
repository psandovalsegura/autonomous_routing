#!/usr/bin/python

#Decentralized Monte Carlo Tree Search algorithm

#This was inspired by:
# Written by Peter Cowling, Ed Powley, Daniel Whitehouse (University of York, UK) September 2012.
#
# Licence is granted to freely use and distribute for any sensible/legal purpose so long as this comment
# remains in any distributed code.

#Rollout initial paths -> Condense paths into best paths -> communicate condensed tree -> replan best path based on other paths

#Edge wait based on expected network congestion, use for score calculation

from math import *
import random
import time
from scipy.spatial.distance import euclidean as dist
import numpy as np

class GameState:
    """ A state of the game, i.e. the game board. These are the only functions which are
        absolutely necessary to implement UCT in any 2-player complete information deterministic
        zero-sum game, although they can be enhanced and made quicker, for example by using a
        GetRandomMove() function to generate a random move during rollout.
        By convention the players are numbered 1 and 2.
    """
    def __init__(self, car, GRID_SIZE, other_cars, penalty = 0):
            self.car = car #current car
            self.other_cars = other_cars #list of cars inside communication radius
            self.other_routes = []
            self.grid_size = GRID_SIZE
            self.pos = self.car.next_intersection.to_tuple() #used to simulate the cars path
            self.goal = self.car.destination.to_tuple()
            self.route = [self.pos]
            self.penalty = penalty #this will be a penalty for having cars on your route

            if self.other_cars != None:
                if len(self.other_cars) > 0:
                    for car in self.other_cars:
                        full_route = [car.route[i].to_tuple() for i in range(len(car.route))]
                        self.other_routes.append(full_route)

    def Clone(self):
        """ Create a deep clone of this game state."""
        st = GameState(self.car, self.grid_size, self.other_cars, self.penalty)
        return st

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved."""

        if len(self.other_routes) > 0:
            try:
                for i in range(len(self.other_routes)):
                    if self.pos == self.other_routes[i][0] and move == self.other_routes[i][1]:# and self.goal == self.other_routes[i][-1]:
                        if self.penalty == 0:
                            self.penalty += 1
                        else:
                            self.penalty = self.penalty + 1 #penalty equivalen of adding another car length
                    if len(self.other_routes[i]) > 0:
                        self.other_routes[i].pop(0)
            except IndexError:
                pass
        self.route.append(move) #update route
        self.pos = move


    def GetMoves(self):
        """ Get all possible moves from this state."""
        moves = []
        next_int = self.pos
        if next_int == self.goal:
            return []
        else:
            #For our case the car can either go East, North, or South
            if next_int[0] + 1 < self.grid_size: #can move east
                moves.append((next_int[0]+1, next_int[1]))
            if (next_int[1] + 1)  < self.grid_size:#can move north
                moves.append((next_int[0], next_int[1]+1))
            if (next_int[1] - 1)  >= 0:#can move south
                moves.append((next_int[0], next_int[1]-1))
            for move in moves:
                if move == self.goal:
                    return [self.goal]
                else:
                    return moves

    def GetResult(self, move):
        #if move is to the goal, end the rollout
        if self.pos == self.goal:
            return 1/(len(self.route)+self.penalty) #rollout score based on distance
        else:
            return 0.0

    def GetRandomMove(self):
        moves = self.GetMoves()
        return random.choice(moves)

    def __repr__(self):
        """ Don't need this - but good style.
        """
        s = "Current Position:" + str(self.pos) + " Goal:" + str(self.goal)
        return s

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves() # future child nodes

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s

def UCT(rootstate, itermax, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state = rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone() #creates a deep copy of the state

        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m,state) # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []: # while state is non-terminal
            state.DoMove(state.GetRandomMove())

        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(state.pos)) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

    # Output some information about the tree - can be omitted
    if (verbose): print(rootnode.TreeToString(0))
    #else: print(rootnode.ChildrenToString())

    return sorted(rootnode.childNodes, key = lambda c: c.wins)[-1].move # return the move that was most visited

def UCTPlayGame(car, GRID_SIZE, other_cars = None):
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = GameState(car, GRID_SIZE, other_cars)
    while (state.GetMoves() != []):
        #print(str(state))
        m = UCT(rootstate = state, itermax = 200, verbose = False) # play with values for itermax and verbose = True
        #print("Best Move: " + str(m) + "\n")
        state.DoMove(m)
    return state.route

def look_ahead(car, network, GRID_SIZE):

    congestion_threshold = 3
    congestion = 0

    if car.next_intersection.to_tuple() == car.destination.to_tuple():
        return False
    if car.remaining_route == []:
        return False
    next_intersection = car.next_intersection.to_tuple()
    possible_nodes = []
    delta_y = car.destination.y - car.next_intersection.y
    delta_x = car.destination.x - car.next_intersection.x

    if car.next_intersection.x > 0:
        node_left = (next_intersection[0] - 1, next_intersection[1])
        if node_left[0] >= 0:
            possible_nodes.append(node_left)
    if delta_x > 0:
        node_right = (next_intersection[0] + 1, next_intersection[1])
        if node_right[0] < GRID_SIZE:
            possible_nodes.append(node_right)
    if delta_y > 0:
        node_up = (next_intersection[0], next_intersection[1] + 1)
        if node_up[1] < GRID_SIZE:
            possible_nodes.append(node_up)
    if delta_y < 0:
        node_down = (next_intersection[0], next_intersection[1] - 1)
        if node_down[1] >= 0:
            possible_nodes.append(node_down)

    if len(possible_nodes) < 2:
        return False
    else:
        for node in possible_nodes:
            try:
                congestion = congestion + network[next_intersection][node]['traffic']
            except KeyError:
                try:
                    congestion = congestion + network[node][next_intersection]['traffic']
                except:
                    continue
            if congestion >= congestion_threshold:
                return True

def update_routes_decmcts(netlogo, cars, GRID_SIZE, network, comm_radius, initial = True):
    #First Loop Updates Paths for the individual car
    #only update this the first time to save on overhead
    if initial:
        for car in cars:
            if car.stopped:# and car.direction == 'east':
                route = UCTPlayGame(car, GRID_SIZE)
                car.push_route_netlogo(netlogo, route, mode = 'both')
    else:
    #Second Loop Communicates route to neighbors and updates its own route
        comm_rad = comm_radius #communications radius for cars ~1.5 road lengths
        dist_array = np.zeros((len(cars),len(cars)))
        for i in range(len(cars)):
            for j in range(len(cars)):
                if i != j:
                    if dist(cars[i].location, cars[j].location) <= comm_rad:
                        dist_array[i][j] = 1
        neighbor_cars = []
        for i, car in enumerate(cars):
            if car.stopped:# or congested:# and
                #if car is near the end, no need to communicate
                if len(car.remaining_route) <= 1:
                    route = UCTPlayGame(car, GRID_SIZE)
                    car.push_route_netlogo(netlogo, route, mode = 'both')
                    continue

                #cars only communicate if the sense congestions
                congested = look_ahead(car, network, GRID_SIZE) #checks to see if the upcoming routes are conjested
                if congested:
                    dist_cars = dist_array[i]
                    #used to find neighbors to communicate with, could also include degredation
                    neighbor_cars = [cars[j] for j, distance in enumerate(dist_cars) if distance != 0]
                    if len(neighbor_cars) > 0:
                        route = UCTPlayGame(car, GRID_SIZE, neighbor_cars)
                        car.push_route_netlogo(netlogo, route, mode = 'both')
                    else:
                        continue

if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players.
    """
    UCTPlayGame()
