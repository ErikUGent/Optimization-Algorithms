"""Vehicles Routing Problem (VRP) with Time Windows."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time

start_time = time.time()

def create_data_model():
    """Stores the data for the problem."""
    '''
    data = {}
    data['time_matrix'] = [
        [0, 6, 9, 8, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7],
        [6, 0, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 10, 14],
        [9, 8, 0, 11, 10, 6, 3, 9, 5, 8, 4, 15, 14, 13, 9, 18, 9],
        [8, 3, 11, 0, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16],
        [7, 2, 10, 1, 0, 6, 9, 4, 8, 9, 13, 4, 6, 8, 12, 8, 14],
        [3, 6, 6, 7, 6, 0, 2, 3, 2, 2, 7, 9, 7, 7, 6, 12, 8],
        [6, 8, 3, 10, 9, 2, 0, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5],
        [2, 4, 9, 6, 4, 3, 6, 0, 4, 4, 8, 5, 4, 3, 7, 8, 10],
        [3, 8, 5, 10, 8, 2, 2, 4, 0, 3, 4, 9, 8, 7, 3, 13, 6],
        [2, 8, 8, 10, 9, 2, 5, 4, 3, 0, 4, 6, 5, 4, 3, 9, 5],
        [6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 0, 10, 9, 8, 4, 13, 4],
        [6, 7, 15, 6, 4, 9, 12, 5, 9, 6, 10, 0, 1, 3, 7, 3, 10],
        [4, 5, 14, 7, 6, 7, 10, 4, 8, 5, 9, 1, 0, 2, 6, 4, 8],
        [4, 8, 13, 9, 8, 7, 10, 3, 7, 4, 8, 3, 2, 0, 4, 5, 6],
        [5, 12, 9, 14, 12, 6, 6, 7, 3, 3, 4, 7, 6, 4, 0, 9, 2],
        [9, 10, 18, 6, 8, 12, 15, 8, 13, 9, 13, 3, 4, 5, 9, 0, 9],
        [7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 0],
    ]   
    data['time_windows'] = [    
        (0, 5),  # depot
        (7, 12),  # 1
        (10, 15),  # 2
        (16, 18),  # 3
        (10, 13),  # 4
        (0, 5),  # 5
        (5, 10),  # 6
        (0, 4),  # 7
        (5, 10),  # 8
        (0, 3),  # 9
        (10, 16),  # 10
        (10, 15),  # 11
        (0, 5),  # 12
        (5, 10),  # 13
        (7, 8),  # 14
        (10, 15),  # 15
        (11, 15),  # 16
    ]

    data['num_vehicles'] = 16
    data['depot'] = 0
    return data

''' 
    data = {}
    data['time_matrix'] = [
 [ 0,  45,  45,  45,  44,  44,  44,  43,  43,  46,  46, 676, 675, 674, 224, 224, 223],
 [ 45,   0,   1,   1,   2,   3,   4,   4,   4,   2,   1, 631, 630, 629, 198, 198, 197],
 [ 45,   1,   0,   1,   1,   2,   3,   3,   4,   3,   2, 632, 631, 630, 199, 198, 197],
 [ 45,   1,   1,   0,   1,   1,   2,   3,   3,   3,   2, 632, 631, 630, 200, 199, 198],
 [ 44,   2,   1,   1,   0,   1,   2,   2,   2,   4,   3, 632, 632, 631, 200, 200, 199],
 [ 44,   3,   2,   1,   1,   0,   1,   1,   2,   5,   4, 633, 632, 631, 201, 200, 199],
 [ 44,   4,   3,   2,   2,   1,   0,   1,   1,   6,   5, 633, 632, 632, 202, 201, 200],
 [ 43,   4,   3,   3,   2,   1,   1,   0,   0,   6,   5, 634, 633, 632, 203, 202, 201],
 [ 43,   4,   4,   3,   2,   2,   1,   0,   0,   6,   6, 634, 633, 633, 203, 202, 201],
 [ 46,   2,   3,   3,   4,   5,   6,   6,   6,   0,   1, 630, 629, 628, 196, 196, 195],
 [ 46,   1,   2,   2,   3,   4,   5,   5,   6,   1,   0, 631, 630, 629, 197, 197, 196],
 [676, 631, 632, 632, 632, 633, 633, 634, 634, 630, 631,   0,   3,   6, 526, 524, 523],
 [675, 630, 631, 631, 632, 632, 632, 633, 633, 629, 630,   3,   0,   3, 524, 522, 521],
 [674, 629, 630, 630, 631, 631, 632, 632, 633, 628, 629,   6,   3,   0, 522, 521, 520],
 [224, 198, 199, 200, 200, 201, 202, 203, 203, 196, 197, 526, 524, 522,   0,   2,   4],
 [224, 198, 198, 199, 200, 200, 201, 202, 202, 196, 197, 524, 522, 521,   2,   0,   2],
 [223, 197, 197, 198, 199, 199, 200, 201, 201, 195, 196, 523, 521, 520,   4,   2,   0],
]
    data['time_windows'] = [    
        (0, 1000),  # depot
        (200, 400),  # 1
        (400, 600),  # 2
        (600, 900),  # 3
        (0, 500),  # 4
        (680, 1200),  # 5
        (900, 1000),  # 6
        (900, 1200),  # 7
        (780, 1400),  # 8
        (900, 1000),  # 9
        (700, 1000),  # 10
        (0, 1000),  # 11
        (200, 1500),  # 12
        (0, 800),  # 13
        (600, 900),  # 14
        (900, 1200),  # 15
        (200, 350),  # 16
    ]
    data['num_vehicles'] = 3
    data['depot'] = 0
    return data

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), solution.Min(time_var),
                solution.Max(time_var))
            index = solution.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),
                                                    solution.Min(time_var),
                                                    solution.Max(time_var))
        plan_output += 'Time of the route: {}min\n'.format(
            solution.Min(time_var))
        print(plan_output)
        total_time += solution.Min(time_var)
    print('Total time of all routes: {}min'.format(total_time))


def main():
    """Solve the VRP with time windows."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time Windows constraint.
    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        9999,  # allow waiting time at the customer
        9999,  # maximum time per vehicle --- > When you want less vehicles
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    depot_idx = data['depot']
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data['time_windows'][depot_idx][0],
            data['time_windows'][depot_idx][1])

    # Instantiate route start and end times to produce feasible times.
    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)


if __name__ == '__main__':
    main()
    print('the elapsed time:%s'% (round(time.time() - start_time, 4)))
