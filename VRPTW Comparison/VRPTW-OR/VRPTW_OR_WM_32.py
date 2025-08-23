"""Vehicles Routing Problem (VRP) with Time Windows."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time

start_time = time.time()

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['time_matrix'] = [       
 [  0,  45,  45,  45,  44,  44,  44,  43,  43,  46,  46, 676, 675, 674, 224, 224, 223, 224, 226, 227, 229, 225, 225, 227, 673, 672, 671, 229, 231, 233, 233, 234, 236],
 [ 45,   0,   1,   1,   2,   3,   4,   4,   4,   2,   1, 631, 630, 629, 198, 198, 197, 198, 199, 201, 202, 200, 199, 201, 629, 628, 627, 206, 208, 211, 208, 210, 212],
 [ 45,   1,   0,   1,   1,   2,   3,   3,   4,   3,   2, 632, 631, 630, 199, 198, 197, 199, 200, 202, 203, 201, 200, 201, 629, 628, 627, 207, 209, 211, 209, 211, 213],
 [ 45,   1,   1,   0,   1,   1,   2,   3,   3,   3,   2, 632, 631, 630, 200, 199, 198, 200, 201, 202, 204, 201, 201, 202, 630, 629, 628, 208, 209, 212, 210, 212, 214],
 [ 44,   2,   1,   1,   0,   1,   2,   2,   2,   4,   3, 632, 632, 631, 200, 200, 199, 200, 201, 203, 204, 202, 201, 203, 630, 629, 628, 208, 210, 213, 210, 212, 215],
 [ 44,   3,   2,   1,   1,   0,   1,   1,   2,   5,   4, 633, 632, 631, 201, 200, 199, 201, 202, 204, 205, 203, 202, 203, 630, 630, 629, 209, 211, 213, 211, 213, 215],
 [ 44,   4,   3,   2,   2,   1,   0,   1,   1,   6,   5, 633, 632, 632, 202, 201, 200, 202, 203, 205, 206, 204, 203, 204, 631, 630, 629, 210, 212, 214, 212, 214, 216],
 [ 43,   4,   3,   3,   2,   1,   1,   0,   0,   6,   5, 634, 633, 632, 203, 202, 201, 202, 203, 205, 207, 204, 204, 205, 632, 631, 630, 210, 212, 215, 212, 214, 217,],
 [ 43,   4,   4,   3,   2,   2,   1,   0,   0,   6,   6, 634, 633, 633, 203, 202, 201, 203, 204, 205, 207, 204, 204, 205, 632, 631, 630, 211, 212, 215, 213, 215, 217,],
 [ 46,   2,   3,   3,   4,   5,   6,   6,   6,   0,   1, 630, 629, 628, 196, 196, 195, 196, 197, 199, 200, 198, 197, 199, 627, 626, 625, 204, 206, 209, 206, 208, 211,],
 [ 46,   1,   2,   2,   3,   4,   5,   5,   6,   1,   0, 631, 630, 629, 197, 197, 196, 197, 198, 200, 201, 199, 198, 200, 628, 627, 626, 205, 207, 209, 207, 209, 211],
 [676, 631, 632, 632, 632, 633, 633, 634, 634, 630, 631,   0,   3,   6, 526, 524, 523, 522, 521, 520, 519, 527, 523, 522,   9,  11,  14, 536, 535, 535, 528, 528, 528],
 [675, 630, 631, 631, 632, 632, 632, 633, 633, 629, 630,   3,   0,   3, 524, 522, 521, 520, 519, 518, 517, 525, 522, 521,   5,   8,  11, 534, 534, 533, 526, 526, 526],
 [674, 629, 630, 630, 631, 631, 632, 632, 633, 628, 629,   6,   3,   0, 522, 521, 520, 519, 518, 517, 515, 523, 520, 519,   2,   5,   8, 532, 532, 532, 525, 525, 525],
 [224, 198, 199, 200, 200, 201, 202, 203, 203, 196, 197, 526, 524, 522, 0,   2,   4,   4,   5,   6,   7,   2,   2,   4, 521, 520, 518,  16, 17,  19,  12,  14,  16],
 [224, 198, 198, 199, 200, 200, 201, 202, 202, 196, 197, 524, 522, 521, 2,   0,   2,   2,   3,   5,   6,   4,   2,   3, 520, 518, 516,  18, 19,  21,  14,  16,  18],
 [223, 197, 197, 198, 199, 199, 200, 201, 201, 195, 196, 523, 521, 520, 4,   2,   0,   2,   3,   4,   6,   6,   3,   4, 518, 517, 515,  20, 21,  23,  16,  18,  20],
 [224, 198, 199, 200, 200, 201, 202, 202, 203, 196, 197, 522, 520, 519, 4,   2,   2,   0,   1,   3,   5,   6,   3,   3, 517, 516, 514,  20, 21,  23,  15,  17,  19],
 [226, 199, 200, 201, 201, 202, 203, 203, 204, 197, 198, 521, 519, 518, 5,   3,   3,   1,   0,   2,   3,   6,   3,   2, 516, 515, 513,  20, 21,  22,  14,  16,  19],
 [227, 201, 202, 202, 203, 204, 205, 205, 205, 199, 200, 520, 518, 517, 6,   5,   4,   3,   2,   0,   2,   7,   4,   3, 515, 514, 512,  20, 21,  22,  14,  16,  18],
 [229, 202, 203, 204, 204, 205, 206, 207, 207, 200, 201, 519, 517, 515, 7,   6,   6,   5,   3,   2,   0,   8,   5,   4, 514, 512, 511,  20, 21,  23,  14,  16,  18],
 [225, 200, 201, 201, 202, 203, 204, 204, 204, 198, 199, 527, 525, 523, 2,   4,   6,   6,   6,   7,   8,   0,   4,   5, 522, 520, 519,  13, 15,  17,  10,  12,  14],
 [225, 199, 200, 201, 201, 202, 203, 204, 204, 197, 198, 523, 522, 520, 2,   2,   3,   3,   3,   4,   5,   4,   0,   1, 519, 517, 516,  17, 18,  20,  12,  14,  17],
 [227, 201, 201, 202, 203, 203, 204, 205, 205, 199, 200, 522, 521, 519, 4,   3,   4,   3,   2,   3,   4,   5,   1,   0, 518, 516, 514,  17, 18,  20,  12,  14,  16],
 [673, 629, 629, 630, 630, 630, 631, 632, 632, 627, 628,   9,   5,   2, 521, 520, 518, 517, 516, 515, 514, 522, 519, 518,   0,   3,   6, 531, 531, 530, 523, 523, 523],
 [672, 628, 628, 629, 629, 630, 630, 631, 631, 626, 627,  11,   8,   5, 520, 518, 517, 516, 515, 514, 512, 520, 517, 516,   3,   0,   3, 529, 529, 529, 522, 522, 522],
 [671, 627, 627, 628, 628, 629, 629, 630, 630, 625, 626,  14,  11,   8, 518, 516, 515, 514, 513, 512, 511, 519, 516, 514,   6,   3,   0, 527, 527, 527, 520, 520, 520],
 [229, 206, 207, 208, 208, 209, 210, 210, 211, 204, 205, 536, 534, 532, 16,  18,  20,  20,  20,  20,  20,  13,  17,  17, 531, 529, 527,   0, 2,   4,   8,   8,   8],
 [231, 208, 209, 209, 210, 211, 212, 212, 212, 206, 207, 535, 534, 532, 17,  19,  21,  21,  21,  21,  21,  15,  18,  18, 531, 529, 527,   2, 0,   3,   8,   7,   8],
 [233, 211, 211, 212, 213, 213, 214, 215, 215, 209, 209, 535, 533, 532, 19,  21,  23,  23,  22,  22,  23,  17,  20,  20, 530, 529, 527,   4, 3,   0,   9,   7,   7],
 [233, 208, 209, 210, 210, 211, 212, 212, 213, 206, 207, 528, 526, 525, 12,  14,  16,  15,  14,  14,  14,  10,  12,  12, 523, 522, 520,   8, 8,   9,   0,   2,   5],
 [234, 210, 211, 212, 212, 213, 214, 214, 215, 208, 209, 528, 526, 525, 14,  16,  18,  17,  16,  16,  16,  12,  14,  14, 523, 522, 520,   8, 7,   7,   2,   0,   2],
 [236, 212, 213, 214, 215, 215, 216, 217, 217, 211, 211, 528, 526, 525, 16,  18,  20,  19,  19,  18,  18,  14,  17,  16, 523, 522, 520,   8, 8,   7,   5,   2,   0],
 ]
  
    data['time_windows'] = [    
        (0, 100),  # depot
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
        (0, 900),  # 17
        (0, 1000),  # 18
        (800, 1000),  # 19
        (600, 700),  # 20
        (500, 900),  # 21
        (200, 300),  # 22
        (650, 800),  # 23
        (700, 1000),  # 24
        (200, 1100),  # 25
        (300, 1400),  # 26
        (800, 1800),  # 27
        (600, 1700),  # 28
        (200, 1250),  # 29
        (800, 1300),  # 30
        (150, 1300),  # 31
        (1500, 2000),  # 32
    ]
    data['num_vehicles'] = 5
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
        1000,  # allow waiting time at the customer
        2000,  # maximum time per vehicle --- > When you want less vehicles
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