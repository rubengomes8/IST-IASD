import sys
from search import *
from itertools import product
import numpy

class ASARProblem(Problem):
    """ Airline Scheduling And Routing """

    airport = {}
    leg = {}
    aircraft = {}
    fleet = []


    def __init__(self):
        Problem.__init__(self, None, None)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
            This should return a set of possible actions for each aircraft.
            An action in this context is defined by a dictionary with actions for each aircraft"""

        if state.aircraft_status is None:
            # Initial State, all of them !airports
            action = iter(list(p for p in product(list(self.airport), repeat=len(self.fleet))))
            print(action)

            return action

        else:

            # Not Initial State
            possible_values = []
            possible_next_airports = set()
            i = 0

            for airplane, values in state.aircraft_status.items():
                possible_values[i] = []
                if values[0] == values[1]: #aeroporto de partida == aeroporto inicial
                    possible_values[i].append(values[0])
                for next_airport, leg, in state.remaining_legs[values[1]].items():
                    # se o tempo permitir adiciona-se a leg
                    minutes_arrival = values[3] + leg[0] #hora do avião + duração de voo
                    print(next_airport)
                    # se o aeroporto fechar antes do voo chegar não se pode adicionar nos possible values
                    # se o aeroporto nao tiver aberto antes do voo chegar talvez se possa adicionar na mesma com um "SINAL"
                    if values[3] is None:
                        if values[4] == 1: #ficou no mesmo sítio
                            break #???
                            pass
                        else:
                            possible_values[i].append(next_airport)
                            possible_next_airports.add(next_airport)
                    else:
                        if minutes_arrival > self.airport[next_airport][0] or minutes_arrival < self.airport[next_airport][1]:
                            possible_values[i].append(next_airport)
                            possible_next_airports.add(next_airport)
                i += 1

            print(possible_values)
            combinations = list(p for p in product(list(possible_next_airports), repeat=len(self.fleet)))
            for comb in combinations:
                for j in range(len(self.fleet)):
                    if comb[j] in possible_values[j]:
                        pass
                    else:
                        combinations.remove(comb)

            print(combinations)
            #falta filtrar as combinações que repetem legs, sem legs disponíveis e retornar as actions que sobraram
            #action = func(possible_values)
            #return action

    def result(self, state, action):
        """Given state and action, return a new state that is the result of the action.
            Action is assumed to be a valid action in the state """
        raise NotImplementedError

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
            if aircraft['base'] != aircraft['cur']:
                return False

        return True

    def path_cost(self, cost_so_far, state1, action, state2):
        raise NotImplementedError

    def value(self, state):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """
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
                self.airport[l_array[1]] = Airport(hour_to_min(l_array[2]), hour_to_min(l_array[3]))

            # Inserts in aircraft dict rotation times
            elif l_array[0] == 'C':
                self.aircraft[l_array[1]] = l_array[2]

            # Inserts a plane in the fleet (reg, class)
            elif l_array[0] == 'P':
                self.fleet.append((l_array[1], l_array[2]))

            # Insert a leg
            elif l_array[0] == 'L':
                leg_counter += 1
                profit = {}
                for i in range(4, len(l_array) - 1, 2):
                    profit[l_array[i]] = int(l_array[i + 1])
                if l_array[1] in self.leg.keys():
                    self.leg[l_array[1]].append(Leg(l_array[2], hour_to_min(l_array[3]), profit))
                else:
                    self.leg[l_array[1]] = []
                    self.leg[l_array[1]].append(Leg(l_array[2], hour_to_min(l_array[3]), profit))


            else:
                raise RuntimeError("Bad Format Error")

        # Construct the Problem
        self.initial = State(None, leg_counter)

        '''for i in self.leg:
            for j in self.leg[i]:
                print("Key:", i, " || ", j)'''

        print(self.leg)
        #print(self.airport)
        '''home_airport = numpy.zeros((len(self.fleet),), dtype=int)
        print(home_airport)'''

        action = set(p for p in product(list(self.airport), repeat=len(self.fleet)))

        print(action)

    def save(self, f, state):
        """saves a solution state s to file f"""

        # No solution was found
        if state is None:
            f.write("Infeasible")
            return


class State:

    def __init__(self, aircraft_status, remaining_legs):
        self.aircraft_status = aircraft_status #dicionario. key: matricula, value:  (aeroporto_inicial, aeroporto_atual, horas_de saida_do aeroporto_anterior, horas_de_saida do aeroporto atual, rtb (return to base))
        self.remaining_legs = remaining_legs  #dicionario. key: DEP, value: (arr, flight_time, profit)


# Class containing information on an Airport
class Airport:

    def __init__(self, open_time, close_time):
        self.open = open_time
        self.close = close_time
        self.legs = []

    def add_leg_to_airport(self, leg):
        self.legs.append(leg)

    def __str__(self):
        return "Open Time: %s || Close Time: %s\n" %(self.open, self.close)



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
        print(asar.airport)

        with open(sys.argv[1]) as f:
            asar.load(f)
            f.close()

    else:
        print("Usage:", sys.argv[0], "<filename>")



if __name__ == '__main__':
    main()
