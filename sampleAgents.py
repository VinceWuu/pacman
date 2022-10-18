# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from operator import le, truediv
from re import search
from pacman import Directions
from game import Agent
import api
import random
import game
import util

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP
    
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)

class GoWestAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        if Directions.WEST not in legal:
            if Directions.NORTH in legal:
                return api.makeMove(Directions.NORTH, legal)
            else:
                return api.makeMove(Directions.SOUTH, legal)
        # Random choice between the legal options.
        return api.makeMove(Directions.WEST, legal)

class CornerSeekingAgent(Agent):

    def __init__(self):
        self.last = Directions.STOP
        self.visited = []

    def getAction(self, state):
        legal = api.legalActions(state)
        currentDirection = state.getPacmanState().configuration.direction
        
        if len(legal) > 3 and api.whereAmI(state) in self.visited:
            return self.foodWithin5(state, currentDirection, legal)
        else:

            self.visited.append(api.whereAmI(state))
            if currentDirection == Directions.STOP:
                currentDirection = Directions.NORTH
            if Directions.LEFT[currentDirection] in legal:
                self.last = Directions.LEFT[currentDirection]
                return self.last
            if currentDirection in legal:
                self.last = currentDirection
                return self.last
            if Directions.RIGHT[currentDirection] in legal:
                self.last = Directions.RIGHT[currentDirection]
                return self.last
            if Directions.LEFT[Directions.LEFT[currentDirection]] in legal:
                self.last = Directions.LEFT[Directions.LEFT[currentDirection]]
                return self.last

    def foodWithin5(self, state, currentDirection, legal):
        cur = api.whereAmI(state)

        for x in range(1, 6):
            #north
            if (cur[0], cur[1]+x) in api.food(state):
                noWall = True
                for y in range(cur[1], cur[1]+x+1):
                    if (cur[0], y) in api.walls(state):
                        noWall = False
                if noWall:
                    last = Directions.NORTH
                    return Directions.NORTH
            #south
            if (cur[0], cur[1]-x) in api.food(state):
                noWall = True
                for y in range(cur[1]-x, cur[1]+1):
                    if (cur[0], y) in api.walls(state):
                        noWall = False
                if noWall:
                    last = Directions.SOUTH
                    return Directions.SOUTH
            #east
            if (cur[0]+x, cur[1]) in api.food(state):
                noWall = True
                for y in range(cur[0], cur[1]+x+1):
                    if (y, cur[1]) in api.walls(state):
                        noWall = False
                if noWall:
                    last = Directions.EAST
                    return Directions.EAST     
            #west
            if (cur[0]-x, cur[1]) in api.food(state):
                noWall = True
                for y in range(cur[0]-x, cur[0]+1):
                    if (y, cur[1]) in api.walls(state):
                        noWall = False
                if noWall:
                    last = Directions.WEST
                    return Directions.WEST

        legal.remove(Directions.STOP)
        self.last = random.choice(legal)
        return self.last

class EatAndRunAgent(Agent):

    def __init__(self):
        self.last = Directions.STOP
        self.visited = []

    def getAction(self, state):
            legal = api.legalActions(state)
            currentDirection = state.getPacmanState().configuration.direction
            if not self.ghostNearBy(state, currentDirection):
                if len(legal) > 3 and api.whereAmI(state) in self.visited:
                    return self.foodWithin5(state, currentDirection, legal)
                else:

                    self.visited.append(api.whereAmI(state))
                    if currentDirection == Directions.STOP:
                        currentDirection = Directions.NORTH
                    if Directions.LEFT[currentDirection] in legal:
                        self.last = Directions.LEFT[currentDirection]
                        return self.last
                    if currentDirection in legal:
                        self.last = currentDirection
                        return self.last
                    if Directions.RIGHT[currentDirection] in legal:
                        self.last = Directions.RIGHT[currentDirection]
                        return self.last
                    if Directions.LEFT[Directions.LEFT[currentDirection]] in legal:
                        self.last = Directions.LEFT[Directions.LEFT[currentDirection]]
                        return self.last
            else:
                return self.avoidGhost(state, currentDirection, legal)

    def foodWithin5(self, state, currentDirection, legal):
        cur = api.whereAmI(state)

        for x in range(1, 6):
            #north
            if (cur[0], cur[1]+x) in api.food(state):
                noWall = True
                for y in range(cur[1], cur[1]+x+1):
                    if (cur[0], y) in api.walls(state):
                        noWall = False
                if noWall:
                    last = Directions.NORTH
                    return Directions.NORTH
            #south
            if (cur[0], cur[1]-x) in api.food(state):
                noWall = True
                for y in range(cur[1]-x, cur[1]+1):
                    if (cur[0], y) in api.walls(state):
                        noWall = False
                if noWall:
                    last = Directions.SOUTH
                    return Directions.SOUTH
            #east
            if (cur[0]+x, cur[1]) in api.food(state):
                noWall = True
                for y in range(cur[0], cur[1]+x+1):
                    if (y, cur[1]) in api.walls(state):
                        noWall = False
                if noWall:
                    last = Directions.EAST
                    return Directions.EAST
            #west
            if (cur[0]-x, cur[1]) in api.food(state):
                noWall = True
                for y in range(cur[0]-x, cur[0]+1):
                    if (y, cur[1]) in api.walls(state):
                        noWall = False
                if noWall:
                    last = Directions.WEST
                    return Directions.WEST

        legal.remove(Directions.STOP)
        self.last = random.choice(legal)
        return self.last

    def ghostNearBy(self, state, currentDirection):
        
        if api.inFront(api.ghosts(state), currentDirection, state):
            return True
        if api.atSide(api.ghosts(state), currentDirection, state):
            return True
        if api.audible(api.ghosts(state), state):
            return True
        return False
    
    def avoidGhost(self, state, currentDirection, legal):
        cur = api.whereAmI(state)
        # if ghosts are in front then turn back 
        if api.inFront(api.ghosts(state), currentDirection, state):
            if Directions.LEFT[Directions.LEFT[currentDirection]] in legal:
                self.last = Directions.LEFT[Directions.LEFT[currentDirection]]
                return self.last

        for x in range(1, 3):
            #north
            if (cur[0], cur[1]+x) in api.ghosts(state):
                noWall = True
                for y in range(cur[1], cur[1]+x+1):
                    if (cur[0], y) in api.walls(state):
                        noWall = False
                if noWall:
                    last = Directions.SOUTH
                    if last in legal:
                        return last
            #south
            if (cur[0], cur[1]-x) in api.ghosts(state):
                noWall = True
                for y in range(cur[1]-x, cur[1]+1):
                    if (cur[0], y) in api.walls(state):
                        noWall = False
                if noWall:
                    last = Directions.NORTH
                    if last in legal:
                        return last
            #east
            if (cur[0]+x, cur[1]) in api.ghosts(state):
                noWall = True
                for y in range(cur[0], cur[1]+x+1):
                    if (y, cur[1]) in api.walls(state):
                        noWall = False
                if noWall:
                    last = Directions.WEST
                    if last in legal:
                        return last    
            #west
            if (cur[0]-x, cur[1]) in api.ghosts(state):
                noWall = True
                for y in range(cur[0]-x, cur[0]+1):
                    if (y, cur[1]) in api.walls(state):
                        noWall = False
                if noWall:
                    last = Directions.EAST
                    if last in legal:
                        return last
        if currentDirection in legal:
            return currentDirection
        else:
            if Directions.LEFT[Directions.LEFT[currentDirection]] in legal:
                self.last = Directions.LEFT[Directions.LEFT[currentDirection]]
                return self.last
        return self.last
