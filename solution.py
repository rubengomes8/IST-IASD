from search import *
import copy

class ASARProblem(Problem):
    """ Airline Scheduling And Routing """

    airport = {}
    leg = {}
    aircraft = {}
    fleet = {}

    def __init__(self):
        Problem.__init__(self, None, None)
        self.max_profit = 0
        self.leg_counter = 0
        self.state_cnt = 0

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
            This should return a set of possible actions for each aircraft.
            An action in this context is defined by a dictionary with actions for each aircraft
            dict. key: reg, value: ([] of (leg, SDT), SDT of base, SDT avail) """

        possible_actions = []

        for plane in self.fleet:
            if state.aircraft_status[plane] is None:
                for legs in state.remaining_legs.values():
                    for leg in legs:
                        # add if leg can be done within airport curfews, need to check conditions
                        #if (self.airport[leg[1]][0] <= self.airport[leg[0]][1] + leg[2] <= self.airport[leg[1]][1]) and (
                              #  self.airport[leg[1]][0] <= self.airport[leg[0]][0] + leg[2] <= self.airport[leg[1]][1]):
                        possible_actions.append(Action(plane, leg))
            else:
                for legs in state.remaining_legs.values():
                    for leg in legs:
                        # Add leg if dep of leg is same of arr of aircraft and aircraft can leave before
                        # closing and aircraft can arrive before closing
                        if leg.dep == state.aircraft_status[plane].legs[-1][0].arr \
                                and state.aircraft_status[plane].sdt_avail + leg.flight_time < self.airport[leg.dep].close_t \
                                and state.aircraft_status[plane].sdt_avail + leg.flight_time <= self.airport[leg.arr].close_t:
                            possible_actions.append(Action(plane, leg))
        return iter(possible_actions)

    def result(self, state, action):
        """Given state and action, return a new state that is the result of the action.
            Action is assumed to be a valid action in the state
            dict. key: reg, value: ([] of (leg, sdt), SDT of base, SDT avail) """

        '''hora abertura aeroporto de saida - duração do voo - hora abertura aeroporto chegada'''
        # Initial state is empty, with children indicating different possible initial states
        if state.aircraft_status[action.aircraft_reg] is None:
            # if the arr airport is still closed if we leave at opening time at dep
            if self.airport[action.leg.dep].open_t + action.leg.flight_time < self.airport[action.leg.arr].open_t:
                departure_time = self.airport[action.leg.arr].open_t - action.leg.flight_time
            else:
                departure_time = self.airport[action.leg.dep].open_t
            leg_completed = []
        else:
            # not an initial state
            departure_time = state.aircraft_status[action.aircraft_reg].sdt_avail
            # prepares new pointer for following state
            leg_completed = copy.deepcopy(state.aircraft_status[action.aircraft_reg].legs)

        # each state has unique status and remaining legs. Deepcopy copies all data to new pointer
        new_aircraft_status = copy.deepcopy(state.aircraft_status)
        new_remaining = copy.deepcopy(state.remaining_legs)

        # removes leg from legs yet to be flown and adds it to the already flown list
        new_remaining[action.leg.dep].remove(action.leg)
        leg_completed.append((action.leg, departure_time))

        # updates status of aircraft that has flown
        next_std_avail = departure_time + action.leg.flight_time + self.aircraft[self.fleet[action.aircraft_reg]]
        new_aircraft_status[action.aircraft_reg] = AircraftStatus(leg_completed, departure_time, next_std_avail)
        self.state_cnt += 1
        return State(new_aircraft_status, new_remaining, state.leg_counter - 1)

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
            state to self.goal or checks for state in self.goal if it is a
            list, as specified in the constructor. Override this method if
            checking against a single self.goal is not enough."""
        # There are still legs left to fly
        if state.leg_counter > 0:
            return False

        # Checks if aircraft base airport is the same as the current airport
        for aircraft_status in state.aircraft_status.values():
            if aircraft_status is None:
                continue
            if aircraft_status.legs[0][0].dep != aircraft_status.legs[-1][0].arr:
                return False
        return True

    def path_cost(self, cost_so_far, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
            state1 via action, assuming cost c to get up to state1. In this case it
            will check the profit obtain from flying the leg taking into account the
            aircraft class. The cost of flying a leg is the max_profit - leg_profit
            which is always > 0."""
        return cost_so_far + self.max_profit - action.leg.get_profit(self.fleet[action.aircraft_reg])

    def heuristic(self, node):
        """h function is straight-line distance from a node's state to goal.
            In this case it will be flying all remaining legs with the class that yields
            best profit. This guarantees we do not overestimate cost. """
        #return 0
        state = node.state

        profit = 0
        for legs1 in state.remaining_legs.values():
            for legs2 in legs1:
                profit += max(legs2.profit.values())

        return len(state.remaining_legs) * self.max_profit - profit

    def load(self, f):
        """Loads a problem from file f"""
        for ln in (ln for ln in f.readlines() if len(ln.split()) > 0):
            l_array = ln.split()
            # Inserts in airport dict curfews
            if l_array[0] == 'A':
                self.airport[l_array[1]] = Airport(l_array[1], hour_to_min(l_array[2]), hour_to_min(l_array[3]))

            # Inserts in aircraft dict rotation times
            elif l_array[0] == 'C':
                self.aircraft[l_array[1]] = hour_to_min(l_array[2])

            # Inserts a plane in the fleet (reg, class)
            elif l_array[0] == 'P':
                self.fleet[l_array[1]] = l_array[2]

            # Insert a leg
            elif l_array[0] == 'L':
                self.leg_counter += 1
                profit = {}
                for i in range(4, len(l_array) - 1, 2):
                    leg_profit = int(l_array[i + 1])
                    profit[l_array[i]] = leg_profit
                    if leg_profit > self.max_profit:
                        self.max_profit = leg_profit
                if l_array[1] in self.leg.keys():
                    self.leg[l_array[1]].append(Leg(l_array[1], l_array[2], hour_to_min(l_array[3]), profit))
                else:
                    self.leg[l_array[1]] = []
                    self.leg[l_array[1]].append(Leg(l_array[1], l_array[2], hour_to_min(l_array[3]), profit))

            else:
                raise RuntimeError("Bad Format Error")

        # Construct the Problem
        initial = State({aircraft: None for aircraft in self.fleet}, self.leg, self.leg_counter)
        self.initial = initial

    def save(self, f, state):
        """saves a solution state s to file f"""
        # No solution was found
        if state is None:
            f.write("Infeasible.")
            return
        else:
            state_c = state.state
            for aircraft, path in state_c.aircraft_status.items():
                if path is not None:
                    schedule = ["S ", aircraft + " "]
                    for flights in iter(path.legs):
                        schedule.append(min_to_hour(flights[1]) + " ")
                        schedule.append(flights[0].dep + " ")
                        schedule.append(flights[0].arr + " ")
                    schedule[-1] = schedule[-1][:-1]

                    [f.writelines(item) for item in schedule]
                    f.write("\n")
            f.write("P " + str((self.max_profit*self.leg_counter - state.path_cost)))


class Action:

    def __init__(self, aircraft_reg, leg):
        self.aircraft_reg = aircraft_reg
        self.leg = leg


class State:

    def __init__(self, aircraft_status, remaining_legs, leg_counter):
        self.aircraft_status = aircraft_status  #dict. key: reg, value: ( []of legs, SDT of base, SDT avail)
        self.remaining_legs = remaining_legs  #dict. key: DEP, value: (arr, flight_time, profit)
        self.leg_counter = leg_counter

    def __lt__(self, other):
        return True

    def __eq__(self, other):
        if isinstance(other, State):
            return self.__dict__ == other.__dict__
        return False

    def __hash__(self):
        return hash(self.leg_counter) ^ hash(tuple(self.aircraft_status))


# Class containing information on a leg.
class Leg:

    def __init__(self, dep, arr, flight_time, profit):
        self.dep = dep
        self.arr = arr
        self.flight_time = flight_time
        self.profit = profit

    def get_profit(self, air_class):
        return self.profit[air_class]

    def __str__(self):
        return "%s -> %s || Flight Time: %s || Profit: %s" % (self.dep, self.arr, self.flight_time, self.profit)

    def __eq__(self, other):
        if isinstance(other, Leg):
            return self.__dict__ == other.__dict__
        return False


class AircraftStatus:

    def __init__(self, legs, sdt_base, sdt_avail):
        self.legs = legs
        self.sdt_base = sdt_base
        self.sdt_avail = sdt_avail

    def __eq__(self, other):
        if isinstance(other, AircraftStatus):
            return self.__dict__ == other.__dict__
        return False


class Airport:

    def __init__(self, a_id, open_t, close_t):
        self.a_id = a_id
        self.open_t = open_t
        self.close_t = close_t


"""Auxiliary Time functions"""


def min_to_hour(minute):
    full_hours = minute//60
    full_minutes = minute % 60
    if full_hours < 10:
        full_hours = "0" + str(full_hours)
    if full_minutes < 10:
        full_minutes = "0" + str(full_minutes)

    return str(full_hours) + str(full_minutes)


def hour_to_min(hours):  # hours in string
    hour = int(hours[0:2])
    minutes = int(hours[2:4])
    return hour * 60 + minutes


"""main"""


def main():
    if len(sys.argv) > 1:
        asar = ASARProblem()

        with open(sys.argv[1], 'r') as f:
            asar.load(f)
            f.close()

        sol_node = astar_search(asar, h=asar.heuristic)  # astar_search return a Node

        print(asar.state_cnt)
        with open("solution.txt", 'w') as f:
            asar.save(f, sol_node)
            f.close()
    else:
        print("Usage:", sys.argv[0], "<filename>")


if __name__ == '__main__':
    main()
