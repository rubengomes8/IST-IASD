import sys
from search import *



class ASARProblem(Problem):
    """ Airline Scheduling And Routing """

    airport = {}
    aircraft = {}
    fleet = []

    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph

    def actions(self, state):
        """ Return the actions that can be executed in the given state."""
        return list(self.graph.get(state).keys())

    def result(self, state, action):
        """Given state and action, return a new state that is the result of the action.
            Action is assumed to be a valid action in the state """
        return tuple(new_state)

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
            state to self.goal or checks for state in self.goal if it is a
            list, as specified in the constructor. Override this method if
            checking against a single self.goal is not enough."""
        return state == self.goal

    def path_cost(self, cost_so_far, state1, action, state2):
        return cost_so_far + (self.graph.get(state1, state2) or infinity)

    def value(self, state):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """
        raise NotImplementedError

    def heuristic(self, node):
        """h function is straight-line distance from a node's state to goal."""
        locs = getattr(self.graph, 'locations', None)
        if locs:
            if type(node) is str:
                return int(distance(locs[node], locs[self.goal]))

            return int(distance(locs[node.state], locs[self.goal]))
        else:
            return infinity

    def load(self,f):
        """Loads a problem from file f"""
        for ln in (ln for ln in f.readlines() if ln.split() > 0):
            l = ln.split()

            # Inserts in airport dict curfews
            if l[0] == 'A':
                self.airport[l[1]] = (l[2],l[3])

            # Inserts in aircraft dict rotation times
            elif l[0] == 'C':
                self.aircraft[l[1]] = l[2]

            # Inserts a plane in the fleet (reg, class)
            elif l[0] == 'P':
                self.fleet.append((l[1],l[2]))

            # Insert a leg
            elif l[0] == 'L':
                values = l.split()

                ## TODO: each aircraft class has different distance cost. Create graph for each class?
                self.graph.connect(l[1],l[2],distance)

            else:
                raise RuntimeError("Bad Format Error")

    def save(self,f, state):
        """saves a solution state s to file f"""

        # No solution was found
        if state is None:
            f.write("Infeasible")
            return

        else:

class Time:

    def min_to_hour(self, min):
        return str(min/60 + min%60)

    def hour_to_min(self, hours): #hours in string
        hour = int(hours[0:1])
        minutes = int(hours[2:3])
        return hour*60+minutes

def main():

    if len(sys.argv) > 1:


        asar = ASARProblem(initial, goal, graph)

        with open(sys.argv[1]) as f:
            asar.load(f)
            f.close()



    else:
        print("Usage:", sys.argv[0], "<filename>")



if __name__ == '__main__':
    main()

