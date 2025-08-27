This repository contains the algorithms and test files used, mdified or created by Erik De Kuyffer in the context of his PhD at the University of Ghent.

In the first project (3 Island Model), Genetic Algorithms are used on a multi-objective island model to optimize simultaneously the distance traveled, the energy required and the lateness of the maintenance planning of offshore windmills. Threedimensional Pareto points are calculated and plotted, each representing a sequence of windmills to be maintained.

The second project contains three comparison methods for solving VRPTW, used in planning optimization for offshore windmill maintenance. It further contains an algorithm to solve the Job Shop Scheduling Problem and the calculation of twodimensional Pareto points to apply both optimization methods (VRPTW and JSSP) simultaneously.

In a third folder, algorithms are used to solve the CVRP to create a planning for multiple vans and for several days. Jobs that need two workers are thereby grouped to the same route. Finally, it contains an algorithm to perform a grid search in order to find the optimal depot location for a set of customers in a predefined grid.

The VShape folder contains an algorithm to determine the optimal configuration in which a group of drones must travel via an optimized route to consume the least amount of energy possible. 

Finally, the XAI folders lists several eXplainable AI techniques used for feature selection. It allows to select the main parameters and/or features for several solution algorithms of three different optimization problems: A newly created Sphere algorithm to solve TSP, the VShape solution method to reduce energy consumption of a flock of drones and the VRPTW solution algorithm for home nurse planning.
