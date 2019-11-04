# IASD
Aritificial Intelligence Project

*Airline Scheduling And Routing*

## Project Description

The main goal of the project is to identify a daily schedule of an Airline's fleet that yields the maximum profit possible, following several constraints, namely Airport Curfews. All legs available must be flown.

The problem is solved using an instance of the A* Search algorithm applied to our problem definition. 

## Problem Definition and Solution

### Describe the state representation and the operators.



### Describe the cost and the heuristic functions.

The cost from flying a leg consists in the profit loss from flying it, such that $cost = 1 + max{profit_of_leg} - actual_profit$. With this function the cost will always increase by atleast 1, with the lower bound cost from the initial state to the goal state being $c = n_legs$ and upper bound being $n_legs + sum{min{profit_of_leg}$, for all legs. The heuristic function is equals to the optimal path from the current state to the goal state, $h(n) = n_remaining_legs$, which intuitively indicates all remaining legs are flown with minimal cost $c = 1$.

### Does the A* algorithm guarantees the optimal solution? Justify.

Yes. This is because our heurisitc algorithm ensures we are not overestimating the cost from the given state to the goal state, therefore making our heuristic admissible. In our case we make the heurisitc function equal to the optimal cost. With an admissible heurisitc, the A* Algorithm will never return a suboptimal solution.

### Determine the number of generated nodes, the depth of the solution, and the effective branching factor, for each one of the example files provided at the course webpage.

