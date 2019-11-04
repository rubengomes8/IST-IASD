# IASD
Aritificial Intelligence Project

*Airline Scheduling And Routing*

## Project Description

The main goal of the project is to identify a daily schedule of an Airline's fleet that yields the maximum profit possible, following several constraints, namely Airport Curfews. All legs available must be flown.

The problem is solved using an instance of the A* Search algorithm applied to our problem definition. 

## Problem Definition and Solution

### Describe the state representation and the operators.


### Describe the cost and the heuristic functions.


### Does the A* algorithm guarantees the optimal solution? Justify.

Yes. This is because our heurisitc algorithm ensures we are not overestimating the cost from the given state to the goal state, therefore making our heuristic admissible. With an admissible heurisitc, the A* Algorithm will never return a suboptimal solution.

### Determine the number of generated nodes, the depth of the solution, and the effective branching factor, for each one of the example files provided at the course webpage.
