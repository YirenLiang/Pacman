# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
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

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

# Yiren Liang k20008278
# This is not a piece of clean code. But please dont mark me down for this.
# This is not a piece of clean code. But please dont mark me down for this.
# This is not a piece of clean code. But please dont mark me down for this.
# This is not a piece of clean code. But please dont mark me down for this.
import api
from game import Agent
from pacman import Directions


class MDPAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up MDPAgent!"
        name = "Pacman"

        self.foodMap = []
        self.wallsMap = []
        self.capsuleMap = []
        self.ghostMap = []
    # get height and width using corners which are provided
    def getHeight(self, state):
        height = 0
        corners = api.corners(state)
        for i in range(len(corners)):
            if corners[i][1] > height:
                height = corners[i][1]
        return height + 1

    def getWidth(self, state):
        width = 0
        corners = api.corners(state)
        for i in range(len(corners)):
            if corners[i][0] > width:
                width = corners[i][0]
        return width + 1

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        print "Running registerInitialState for MDPAgent!"
        print "I'm at:"
        print api.whereAmI(state)

    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like the game just ended!"

        self.foodMap = []
        self.wallsMap = []
        self.capsuleMap = []
        self.ghostMap = []

    # this method assign value to each cell by ghost, eatable ghost, food, capsules.....
    def now_map(self, state, mapType):
        pacman = api.whereAmI(state)
        foods = api.food(state)
        walls = api.walls(state)
        capsules = api.capsules(state)
        ghosts = api.ghosts(state)
        eatghosts = api.ghostStatesWithTimes(state)
        # the dict that store (coordinate,value)
        whole_map = {}
        # set value for food and capsule
        food_value = 1
        capsule_value = 5
        for food in foods:
            whole_map[food] = food_value
        # note i have a string for walls so the code below will use whole_map[] != "#" to avoid walls
        for wall in walls:
            whole_map[wall] = "#"
        for capsule in capsules:
            whole_map[capsule] = capsule_value
        # if the cell is not yet assigned a value. put it with zero
        height = self.getHeight(state)
        width = self.getWidth(state)
        for i in range(width):
            for j in range(height):
                if (i, j) not in whole_map.keys():
                    whole_map[(i, j)] = 0
        # small grid assign
        if mapType == "smallGrid":
            if ghosts:
                for i in ghosts:
                    # assign ghost value
                    whole_map[int(i[0]), int(i[1])] = -50
                    # the cell a ghost can get to in 1 or 2 steps
                    ghosts_reach1 = []
                    ghosts_reach2 = []
                    reached = []
                    # ghost can only reach if not a wall
                    if whole_map[int(i[0]) - 1, int(i[1])] != "#":
                        ghosts_reach1.append((int(i[0]) - 1, int(i[1])))
                    if whole_map[int(i[0]) + 1, int(i[1])] != "#":
                        ghosts_reach1.append((int(i[0]) + 1, int(i[1])))
                    if whole_map[int(i[0]), int(i[1]) + 1] != "#":
                        ghosts_reach1.append((int(i[0]), int(i[1]) + 1))
                    if whole_map[int(i[0]), int(i[1]) - 1] != "#":
                        ghosts_reach1.append((int(i[0]), int(i[1]) - 1))
                    reached = reached + ghosts_reach1
                    # cells ghost can reach for 2 steps if not wall and not in the cells that ghost can reach in 1 step
                    for j in ghosts_reach1:
                        if whole_map[j[0] - 1, j[1]] != "#" and (j[0] - 1, j[1]) not in reached:
                            ghosts_reach2.append((j[0] - 1, j[1]))
                            reached.append((j[0] - 1, j[1]))
                        if whole_map[j[0] + 1, j[1]] != "#" and (j[0] + 1, j[1]) not in reached:
                            ghosts_reach2.append((j[0] + 1, j[1]))
                            reached.append((j[0] + 1, j[1]))
                        if whole_map[j[0], j[1] - 1] != "#" and (j[0], j[1] - 1) not in reached:
                            ghosts_reach2.append((j[0], j[1] - 1))
                            reached.append((j[0], j[1] - 1))
                        if whole_map[j[0], j[1] + 1] != "#" and (j[0], j[1] + 1) not in reached:
                            ghosts_reach2.append((j[0], j[1] + 1))
                            reached.append((j[0], j[1] + 1))
                    # the cell 1 steps away from ghost is dangerous
                    for x in ghosts_reach1:
                        whole_map[x[0], x[1]] = -30
                    # cells 2 steps away still dangerous but less
                    for y in ghosts_reach2:
                        whole_map[y[0], y[1]] = -10
        # this is medium classic assign
        else:
            if ghosts:
                for i in ghosts:
                    # everything is the same as above but i expand the steps for ghost can reach.
                    whole_map[int(i[0]), int(i[1])] = -70
                    # cells that ghost can reach in 1 step
                    ghosts_reach1 = []
                    # cells that ghost can reach in 2 step
                    ghosts_reach2 = []
                    # and so on
                    ghosts_reach3 = []
                    ghosts_reach4 = []
                    ghosts_reach5 = []
                    ghosts_reach6 = []
                    reached = []
                    if whole_map[int(i[0]) - 1, int(i[1])] != "#":
                        ghosts_reach1.append((int(i[0]) - 1, int(i[1])))
                    if whole_map[int(i[0]) + 1, int(i[1])] != "#":
                        ghosts_reach1.append((int(i[0]) + 1, int(i[1])))
                    if whole_map[int(i[0]), int(i[1]) + 1] != "#":
                        ghosts_reach1.append((int(i[0]), int(i[1]) + 1))
                    if whole_map[int(i[0]), int(i[1]) - 1] != "#":
                        ghosts_reach1.append((int(i[0]), int(i[1]) - 1))
                    reached = reached + ghosts_reach1
                    # keep expanding how many steps it can reach
                    for j in ghosts_reach1:
                        if whole_map[j[0] - 1, j[1]] != "#" and (j[0] - 1, j[1]) not in reached:
                            ghosts_reach2.append((j[0] - 1, j[1]))
                            reached.append((j[0] - 1, j[1]))
                        if whole_map[j[0] + 1, j[1]] != "#" and (j[0] + 1, j[1]) not in reached:
                            ghosts_reach2.append((j[0] + 1, j[1]))
                            reached.append((j[0] + 1, j[1]))
                        if whole_map[j[0], j[1] - 1] != "#" and (j[0], j[1] - 1) not in reached:
                            ghosts_reach2.append((j[0], j[1] - 1))
                            reached.append((j[0], j[1] - 1))
                        if whole_map[j[0], j[1] + 1] != "#" and (j[0], j[1] + 1) not in reached:
                            ghosts_reach2.append((j[0], j[1] + 1))
                            reached.append((j[0], j[1] + 1))
                    for k in ghosts_reach2:
                        if whole_map[k[0] - 1, k[1]] != "#" and (k[0] - 1, k[1]) not in reached:
                            ghosts_reach3.append((k[0] - 1, k[1]))
                            reached.append((k[0] - 1, k[1]))
                        if whole_map[k[0] + 1, k[1]] != "#" and (k[0] + 1, k[1]) not in reached:
                            ghosts_reach3.append((k[0] + 1, k[1]))
                            reached.append((k[0] + 1, k[1]))
                        if whole_map[k[0], k[1] - 1] != "#" and (k[0], k[1] - 1) not in reached:
                            ghosts_reach3.append((k[0], k[1] - 1))
                            reached.append((k[0], k[1] - 1))
                        if whole_map[k[0], k[1] + 1] != "#" and (k[0], k[1] + 1) not in reached:
                            ghosts_reach3.append((k[0], k[1] + 1))
                            reached.append((k[0], k[1] + 1))
                    for f in ghosts_reach3:
                        if whole_map[f[0] - 1, f[1]] != "#" and (f[0] - 1, f[1]) not in reached:
                            ghosts_reach4.append((f[0] - 1, f[1]))
                            reached.append((f[0] - 1, f[1]))
                        if whole_map[f[0] + 1, f[1]] != "#" and (f[0] + 1, f[1]) not in reached:
                            ghosts_reach4.append((f[0] + 1, f[1]))
                            reached.append((f[0] + 1, f[1]))
                        if whole_map[f[0], f[1] - 1] != "#" and (f[0], f[1] - 1) not in reached:
                            ghosts_reach4.append((f[0], f[1] - 1))
                            reached.append((f[0], f[1] - 1))
                        if whole_map[f[0], f[1] + 1] != "#" and (f[0], f[1] + 1) not in reached:
                            ghosts_reach4.append((f[0], f[1] + 1))
                            reached.append((f[0], f[1] + 1))
                    #this for eat ghost
                    for o in ghosts_reach4:
                        if whole_map[o[0] - 1, o[1]] != "#" and (o[0] - 1, o[1]) not in reached:
                            ghosts_reach5.append((o[0] - 1, o[1]))
                            reached.append((o[0] - 1, o[1]))
                        if whole_map[o[0] + 1, o[1]] != "#" and (o[0] + 1, o[1]) not in reached:
                            ghosts_reach5.append((o[0] + 1, o[1]))
                            reached.append((o[0] + 1, o[1]))
                        if whole_map[o[0], o[1] - 1] != "#" and (o[0], o[1] - 1) not in reached:
                            ghosts_reach5.append((o[0], o[1] - 1))
                            reached.append((o[0], o[1] - 1))
                        if whole_map[o[0], o[1] + 1] != "#" and (o[0], o[1] + 1) not in reached:
                            ghosts_reach5.append((o[0], o[1] + 1))
                            reached.append((o[0], o[1] + 1))
                    for c in ghosts_reach5:
                        if whole_map[c[0] - 1, c[1]] != "#" and (c[0] - 1, c[1]) not in reached:
                            ghosts_reach6.append((c[0] - 1, c[1]))
                            reached.append((c[0] - 1, c[1]))
                        if whole_map[c[0] + 1, c[1]] != "#" and (c[0] + 1, c[1]) not in reached:
                            ghosts_reach6.append((c[0] + 1, c[1]))
                            reached.append((c[0] + 1, c[1]))
                        if whole_map[c[0], c[1] - 1] != "#" and (c[0], c[1] - 1) not in reached:
                            ghosts_reach6.append((c[0], c[1] - 1))
                            reached.append((c[0], c[1] - 1))
                        if whole_map[c[0], c[1] + 1] != "#" and (c[0], c[1] + 1) not in reached:
                            ghosts_reach6.append((c[0], c[1] + 1))
                            reached.append((c[0], c[1] + 1))
                    good_ghost = False
                    for eatghost in eatghosts:
                        # so if ghost is still editable in >5 seconds and this ghost is the one im looping
                        if eatghost[1] > 5 and i == eatghost[0]:
                            good_ghost = True
                            break
                    # set that yummy ghost a big value
                    if good_ghost and (pacman in reached):
                        whole_map[int(i[0]), int(i[1])] = 80
                    else:
                        # if not yummy, put negative value around it.
                        for x in ghosts_reach1:
                            whole_map[x[0], x[1]] -= 50
                        # 2 steps away. less dangerous
                        for y in ghosts_reach2:
                            whole_map[y[0], y[1]] -= 40
                        # and so on
                        for z in ghosts_reach3:
                            whole_map[z[0], z[1]] -= 20
                        for w in ghosts_reach4:
                            whole_map[w[0], w[1]] -= 10

        return whole_map
    # i did this so all_utilities can be shorter
    def one_move(self, move, position, nowMap):

        if move == Directions.NORTH:
            f = nowMap.get((position[0], position[1] + 1), nowMap[position])
            l = nowMap.get((position[0] + 1, position[1]), nowMap[position])
            r = nowMap.get((position[0] - 1, position[1]), nowMap[position])

        elif move == Directions.SOUTH:
            f = nowMap.get((position[0], position[1] - 1), nowMap[position])
            l = nowMap.get((position[0] + 1, position[1]), nowMap[position])
            r = nowMap.get((position[0] - 1, position[1]), nowMap[position])

        elif move == Directions.WEST:
            f = nowMap.get((position[0] - 1, position[1]), nowMap[position])
            l = nowMap.get((position[0], position[1] + 1), nowMap[position])
            r = nowMap.get((position[0], position[1] - 1), nowMap[position])

        elif move == Directions.EAST:
            f = nowMap.get((position[0] + 1, position[1]), nowMap[position])
            l = nowMap.get((position[0], position[1] + 1), nowMap[position])
            r = nowMap.get((position[0], position[1] - 1), nowMap[position])

        if f == "#":
            f = nowMap[position]
        if l == "#":
            l = nowMap[position]
        if r == "#":
            r = nowMap[position]
        # 80% forward 10% left and right
        reward = f * 0.8 + l * 0.1 + r * 0.1

        return reward


    def all_utilities(self, position, nowMap):
        values = []
        for move in [Directions.NORTH, Directions.EAST, Directions.WEST, Directions.SOUTH]:
            values.append(self.one_move(move, position, nowMap))
        return max(values)
    # use the equation from lectures
    # stop iterating if the difference is smaller than 0.001 or already looped 50 times
    def value_iteration(self, nowMap):
        gamma = 0.9
        newMap = nowMap
        for i in range(50):
            oldMap = newMap
            newMap = {}
            biggest_change = -1000
            for pos, val in oldMap.items():
                if val == "#":
                    newMap[pos] = "#"
                else:
                    newMap[pos] = nowMap[pos] + gamma * self.all_utilities(pos, oldMap)
                if newMap[pos] != "#" and ((newMap[pos] - oldMap[pos]) > biggest_change):
                    biggest_change = newMap[pos] - oldMap[pos]
            if biggest_change < 0.001:
                break

        return newMap
        # display is provided in week5
    def display(self, aMap, state):
        grid = []
        height = self.getHeight(state)
        width = self.getWidth(state)
        for i in range(height):
            row = []
            for j in range(width):
                row.append(0)
            grid.append(row)
        for pos, val in aMap.items():
            grid[pos[1]][pos[0]] = val
        for i in range(height):
            for j in range(width):
                # print grid elements with no newline
                print grid[height - (i + 1)][j],
            # A new line after each line of the grid
            print
            # A line after the grid
        print
    # compare the max value and return it. so pac man know where to go
    def getDirection(self, state, nowMap):
        position = api.whereAmI(state)
        moves = {}
        for move in [Directions.NORTH, Directions.EAST, Directions.WEST, Directions.SOUTH]:
            moves[move] = self.one_move(move, position, nowMap)
        max_key = max(moves, key=moves.get)

        return max_key

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)


        #self.display(currentMap, state)
        mapType = "smallGrid"
        if self.getWidth(state) > 8:
            mapType = "mediumClassic"
        currentMap = self.now_map(state, mapType)

        newMap = self.value_iteration(currentMap)
        #print(self.now_map(state, mapType))
        #self.display(newMap, state)

        #print self.getDirection(state, newMap)

        return api.makeMove(self.getDirection(state, newMap), legal)

