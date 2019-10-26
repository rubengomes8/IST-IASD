import sys
from search import *
from itertools import product
import numpy

class ASARProblem(Problem):
    """ Airline Scheduling And Routing """

    airport = {}
    leg = {}
    aircraft = {}
    fleet = {}

    def __init__(self):
        Problem.__init__(self, None, None)
        self.max_profit = 0

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
            This should return a set of possible actions for each aircraft.
            An action in this context is defined by a dictionary with actions for each aircraft
            dict. key: reg, value: ([] of legs, SDT of base, SDT avail) """

        possible_actions = []

        for plane in self.fleet:
            if state.aircraft_status[plane[0]] is None:
                for legs in self.leg.values():
                    for leg in legs:
                        possible_actions.append((plane[0], leg))
            else:
                for legs in state.remaining_legs.values():
                    for leg in legs:
                        if leg[0] == state.aircraft_status[plane[0]][0][-1][1] and state.aircraft_status[plane[0]][2]< \
                                self.airport[leg[0]][1] and state.aircraft_status[plane[0]][2] + leg[2] <=\
                                self.airport[leg[1]][1] :
                            possible_actions.append((plane[0], leg))

        return (possible_actions)

    def result(self, state, action):
        """Given state and action, return a new state that is the result of the action.
            Action is assumed to be a valid action in the state
            dict. key: reg, value: ([] of legs, SDT of base, SDT avail) """

        '''hora abertura aeroporto de saida - duração do voo - hora abertura aeroporto chegada'''
        if state.aircraft_status[action[0]] is None:
            if self.airport[action[1][0]][0]+ action[1][2]< self.airport[action[1][1]][0] :
                departure_time = self.airport[action[1][0]][0] + (self.airport[action[1][1]][0] - (self.airport[action[1][0]][0]+ action[1][2]))
                next_possible_time = departure_time + action[1][2] + self.aircraft[self.fleet[action[0]]]

                legcompleted=[]
                aircraftstatus={}
                new_remaining = state.remaining_legs
                new_remaining[action[1][0]].remove(action[1])

                legcompleted.append(action[1])
                aircraftstatus[action[0]] = (legcompleted, departure_time, next_possible_time)
                return State(aircraftstatus, new_remaining)
        else:
            departure_time = state.aircraft_status[action[0]][2]
            next_possible_time = departure_time + action[1][2] + self.aircraft[self.fleet[action[0]]]

            legcompleted = state.aircraft_status[action[0]][0]
            aircraftstatus = {}
            new_remaining = state.remaining_legs
            new_remaining[action[1][0]].remove(action[1])

            legcompleted.append(action[1])
            aircraftstatus[action[0]] = (legcompleted, departure_time, next_possible_time)
            return State(aircraftstatus, new_remaining)




    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
            state to self.goal or checks for state in self.goal if it is a
            list, as specified in the constructor. Override this method if
            checking against a single self.goal is not enough."""

        # There are still legs left to fly
        if len(state.remaining_legs) > 0:
            return False

        # Checks if aircraft base airport is the same as the current airport
        for aircraft in state.aircraft_status.values():
            if aircraft[0] != aircraft[1]:
                return False

        return True

    def path_cost(self, cost_so_far, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return cost_so_far + self.max_profit - action[1][2]  # check action structure

    def value(self, state):
        """For optimization problems, each state has a value. Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError

    def heuristic(self, state):
        """h function is straight-line distance from a node's state to goal."""
        raise NotImplementedError

    def load(self, f):
        """Loads a problem from file f"""
        leg_counter = 0
        for ln in (ln for ln in f.readlines() if len(ln.split()) > 0):
            l_array = ln.split()
            # Inserts in airport dict curfews
            if l_array[0] == 'A':
                self.airport[l_array[1]] = (hour_to_min(l_array[2]), hour_to_min(l_array[3]))

            # Inserts in aircraft dict rotation times
            elif l_array[0] == 'C':
                self.aircraft[l_array[1]] = hour_to_min(l_array[2])

            # Inserts a plane in the fleet (reg, class)
            elif l_array[0] == 'P':
                self.fleet[l_array[1]]= l_array[2]

            # Insert a leg
            elif l_array[0] == 'L':
                leg_counter += 1
                profit = {}
                for i in range(4, len(l_array) - 1, 2):
                    leg_profit = int(l_array[i + 1])
                    profit[l_array[i]] = leg_profit
                    if leg_profit > self.max_profit:
                        self.max_profit = leg_profit
                if l_array[1] in self.leg.keys():
                    self.leg[l_array[1]].append((l_array[1], l_array[2], hour_to_min(l_array[3]), profit))
                else:
                    self.leg[l_array[1]] = []
                    self.leg[l_array[1]].append((l_array[1], l_array[2], hour_to_min(l_array[3]), profit))

            else:
                raise RuntimeError("Bad Format Error")
        print(self.airport)
        print(self.aircraft)
        print(self.fleet)






        # Construct the Problem
        self.initial = State(None, self.leg)


    def save(self, f, state):
        """saves a solution state s to file f"""
        # No solution was found
        if state is None:
            f.write("Infeasible.")
            return
        else:
            for aircraft in state.aircraft_status.values():
                pass



class State:

    def __init__(self, aircraft_status, remaining_legs):
        self.aircraft_status = aircraft_status  #dict. key: reg, value: ( []of legs, SDT of base, SDT avail)
        self.remaining_legs = remaining_legs  #dict. key: DEP, value: (arr, flight_time, profit)


# Class containing information on a leg.
class Leg:

    def __init__(self, arr, flight_time, profit):
        self.arr = arr
        self.flight_time = flight_time
        self.profit = profit

    def __str__(self):
        return "Arrival Airport: %s || Flight Time: %s || Profit: %s\n" % (self.arr, self.flight_time, self.profit)

    # Returns arrival airport, time of arrival and profit of given leg
    def calculate_route(self, a_class, std):
        return self.arr, std + self.flight_time, self.profit[a_class]


# Auxiliary Time functions

def min_to_hour(minute):
    return str(minute / 60 + minute % 60)


def hour_to_min(hours):  # hours in string
    hour = int(hours[0:2])
    minutes = int(hours[2:4])
    return hour * 60 + minutes


def main():
    if len(sys.argv) > 1:
        asar = ASARProblem()
        #print(asar.airport)

        with open(sys.argv[1],'r') as f:
            asar.load(f)
            f.close()
'''
        sol_node = astar_search(asar, h=None)  # astar_search return a Node

        with open("solution.txt", 'w') as f:
            asar.save(f, sol_node.state())
            f.close()
    else:
        print("Usage:", sys.argv[0], "<filename>")
'''

if __name__ == '__main__':
    main()
