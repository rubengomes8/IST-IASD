# IASD
Aritificial Intelligence Project

*Airline Scheduling And Routing*

## Project Description

The main goal of the project is to identify a daily schedule of an Airline's fleet that yields the maximum profit possible, following several constraints, namely Airport Curfews. All legs available must be flown.

The problem is solved using an instance of the A* Search algorithm applied to our problem definition. 

## Problem Definition and Solution

### Describe the state representation and the operators.

Um estado é caraterizado por uma lista de legs percorridas por cada avião (indexada pela matrícula) o tempo de partida da base e o tempo em que o avião estará disponível para realizar a próxima viagem. É também caraterizado pelo profit obtido até ao momento, pelo número de legs que falta percorrer e pela lista de legs que falta percorrer, em que cada leg é indexada pelo aeroporto de partida e tem como valores o aeroporto de chegada, a duração de voo e o profit. Dado um estado, verifica-se todas as possibilidades válidas de voo de cada avião nas legs que ainda falta percorrer, obtendo-se assim todas as possibilidades compatíveis para o estado seguinte que correspondem ao voo de um único avião.

### Describe the cost and the heuristic functions.

The cost from flying a leg consists in the profit loss from flying it, such that cost = 1 + max{profit_of_leg} - actual_profit. With this function the cost will always increase by at least 1, with the lower bound cost from the initial state to the goal state being c = n_legs and upper bound being n_legs + sum{min{profit_of_leg}, for all legs. The heuristic function is equals to the optimal path from the current state to the goal state, h(n) = n_remaining_legs, which intuitively indicates all remaining legs are flown with minimal cost c = 1.

(Rúben) O custo entre o estado 1 e 2 é a soma do custo no estado 1 com o custo de realizar a ação que leva ao estado 2, que neste caso é um avião ter percorrido uma leg. O custo associado a um avião ter percorrido uma leg é 1 + "a diferença entre o máximo profit dessa leg e o profit obtido ao percorrer essa leg pela classe do avião que a percorreu". Esta definição de custo resulta num custo máximo de 1*(#legs). A heurística é dada pelo número de legs que falta percorrer que corresponde ao custo mínimo desde aquele estado até ao goal state.

### Does the A* algorithm guarantees the optimal solution? Justify.

Yes. This is because our heurisitc algorithm ensures we are not overestimating the cost from the given state to the goal state, therefore making our heuristic admissible. In our case we make the heurisitc function equal to the optimal cost. With an admissible heurisitc, the A* Algorithm will never return a suboptimal solution.

Tradução - Sim. Isto porque a nossa heurstica garante que não se sobreestima o custo de um estado até ao estado goal, tornando-a admissível. No nosso caso a função heurística é igual ao custo ótimo. Com uma heurstica admissvel, o algoritmo de procura A* retorna sempre a solução ótima.

### Determine the number of generated nodes, the depth of the solution, and the effective branching factor, for each one of the example files provided at the course webpage.



