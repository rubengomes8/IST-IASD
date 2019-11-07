# IASD
Aritificial Intelligence Project

*Airline Scheduling And Routing*

## Project Description

The main goal of the project is to identify a daily schedule of an Airline's fleet that yields the maximum profit possible, following several constraints, namely Airport Curfews. All legs available must be flown.

The problem is solved using an instance of the A* Search algorithm applied to our problem definition. 

## Problem Definition and Solution

### Describe the state representation and the operators.

A state is characterized by the status of each aircraft(indexed by registration) that includes a list of legs flown, the departure time from the base airport and the available time for the next departure. It is also characterized by the profit obtained so fair and the number and the remaining legs to be flown. This is represented by a dictionary that is indexed by the departing airport and has as values the arrival airport, flight duration and profit. Given a state, all valid possibilities of flights for each aircraft are checked against the remaining legs, obtaining a set of valid actions to be performed, in this case, a single flight being flown by a single aircraft. The initial state of the problem is not unique, meaning multiple initial states exist(a state for each leg, for each aircraft), therefore the initial state is represented by a lack of aircraft status.

### Describe the cost and the heuristic functions.

The cost from flying a leg consists of the profit loss from flying it, such that cost = 1 + max{profit_of_leg} - actual_profit. With this function, the cost will always increase by at least 1, with the lower bound cost from the initial state to the goal state being c = n_legs and upper bound being n_legs + sum{min{profit_of_leg}, for all legs. The heuristic function is equal to the optimal path from the current state to the goal state, h(n) = n_remaining_legs, which intuitively indicates all remaining legs are flown with minimal cost c = 1.

### Does the A* algorithm guarantees the optimal solution? Justify.

Yes. This is because our heuristic algorithm ensures we are not overestimating the cost from the given state to the goal state, therefore making our heuristic admissible. In our case, we make the heuristic function equal to the optimal cost. With an admissible heuristic, the A* Algorithm will never return a suboptimal solution.

### Determine the number of generated nodes, the depth of the solution, and the effective branching factor, for each one of the example files provided at the course webpage.

simple 1 - genereated nodes - 40 ; depth of solution: 6; 40 = 1 + x + x² + x³ + x⁴ + x⁵ + x⁶ -> x=1.574 ; 
simple 2 - genereated nodes - 61 ; depth of solution: 8; 61 = 1 + x + x² + x³ + x⁴ + x⁵ + x⁶+ x⁷+ x⁸ -> x=1.451; 
simple 3 - genereated nodes - 26 ; depth of solution: 4; 26 = 1 + x + x² + x³ + x⁴ -> x=1.891; 
simple 4 - genereated nodes - 47 ; depth of solution: 6; 47 = 1 + x + x² + x³ + x⁴ + x⁵ + x⁶ -> x=1.630; 
simple 5 - genereated nodes - 69 ; depth of solution: 8; 69 = 1 + x+ x² + x³ + x⁴ + x⁵ + x⁶+ x⁷+ x⁸ -> x=1.480; 
simple 6 - genereated nodes - 606 ; depth of solution: 6; 606 = 1 + x+ x² + x³ + x⁴ + x⁵ + x⁶-> x=2.693; 
simple 7 - genereated nodes - 540 ; depth of solution: 6; 540 = 1 + x+ x² + x³ + x⁴ + x⁵ + x⁶ -> x=2.636 ; 
simple 8 - genereated nodes - 105 ; depth of solution: 8; 105 = 1 + x+ x² + x³ + x⁴ + x⁵ + x⁶+ x⁷+ x⁸ -> x=1.582; 



