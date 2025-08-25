# CVRP application for creating a planning for a VAR for one day for 5 vans with a previously calaculated distance matrix
# Jobs that need two workers are added to the same route

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np


def create_data_model():
    data = {}
    data['distance_matrix'] = [
        [  0,  82,  47, 108, 136,   6,   4,  42,  54,  54,  57,  65,  75,  10,   5,  47,  12],
        [ 82,   0, 128, 184, 211,  81,  78,  63, 135,  27,  25, 140, 154,  79,  78,  39,  81],
        [ 47, 128,   0,  67,  93,  47,  50,  78,  12, 101, 103,  31,  33,  50,  50,  91,  48],
        [108, 184,  67,   0,  28, 105, 110, 123,  70, 157, 160,  44,  34, 107, 109, 145, 104],
        [136, 211,  93,  28,   0, 133, 138, 151,  95, 185, 188,  72,  61, 135, 137, 172, 132],
        [  6,  81,  47, 105, 133,   0,   5,  37,  55,  54,  57,  62,  73,   4,   4,  45,   5],
        [  4,  78,  50, 110, 138,   5,   0,  39,  57,  51,  53,  66,  77,   7,   2,  43,  10],
        [ 42,  63,  78, 123, 151,  37,  39,   0,  88,  41,  44,  81,  96,  33,  37,  25,  33],
        [ 54, 135,  12,  70,  95,  55,  57,  88,   0, 108, 110,  39,  37,  59,  57, 100,  57],
        [ 54,  27, 101, 157, 185,  54,  51,  41, 108,   0,   3, 114, 127,  51,  51,  16,  54],
        [ 57,  25, 103, 160, 188,  57,  53,  44, 110,   3,   0, 116, 129,  54,  53,  19,  57],
        [ 65, 140,  31,  44,  72,  62,  66,  81,  39, 114, 116,   0,  16,  63,  66, 101,  60],
        [ 75, 154,  33,  34,  61,  73,  77,  96,  37, 127, 129,  16,   0,  75,  77, 115,  72],
        [ 10,  79,  50, 107, 135,   4,   7,  33,  59,  51,  54,  63,  75,   0,   6,  41,   4],
        [  5,  78,  50, 109, 137,   4,   2,  37,  57,  51,  53,  66,  77,   6,   0,  43,   8],
        [ 47,  39,  91, 145, 172,  45,  43,  25, 100,  16,  19, 101, 115,  41,  43,   0,  44],
        [ 12,  81,  48, 104, 132,   5,  10,  33,  57,  54,  57,  60,  72,   4,   8,  44,   0],
    ]
    data['demands'] = [0, 45, 120, 60, 0, 90, 120, 120, 30, 120, 0, 150, 120, 90, 120, 90, 45]
    data['time_matrix'] = np.array(data['distance_matrix']) + data['demands']
    data['num_vehicles'] = 5
    data['depot'] = 0
    data['two_workers'] = [1, 5, 8]
    data['vehicle_capacities'] = [390, 390, 390, 390, 390]
    data['starts'] = [0, 10, 0, 0, 0]
    data['ends'] = [0, 10, 0, 0, 0]
    return data

def print_solution(data, manager, routing, assignment):
    print(f'Objective: {assignment.ObjectiveValue()}')

    dropped_nodes = 'Dropped nodes:'
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if assignment.Value(routing.NextVar(node)) == node:
            dropped_nodes += ' {}'.format(manager.IndexToNode(node))
    print(dropped_nodes)

    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Time of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total Distance of all routes: {}m'.format(total_distance))
    print('Total Load of all routes: {}'.format(total_load))


def main():
    data = create_data_model()

    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']),
                                           data['num_vehicles'], data['starts'],
                                           data['ends'])

    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        # Returns the distance between the two nodes.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time Dimension: The total route + work cannot be longer than 480min (8h work)
    routing.AddDimension(
        transit_callback_index,
        0,  # null capacity slack
        480,  # vehicle maximum time of route
        True,  # start cumul to zero
        'Time',)

    time_dimension = routing.GetDimensionOrDie('Time')
    time_dimension.SetGlobalSpanCostCoefficient(100)
    
    def demand_callback(from_index):
        # Returns the demand of the node.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')
    
    # Allow to drop nodes.
    penalty = 50000
    for node in range(1, len(data['time_matrix'])):
        routing.AddDisjunction([manager.NodeToIndex(node)], penalty)

    # Assign jobs for two workers to the same vehicle
    for node in range(1, len(data['time_matrix'])):
        if node in data['two_workers']:
            index =  manager.NodeToIndex(node)
            routing.VehicleVar(index).SetValues([0])
        else:  
            index =  manager.NodeToIndex(node)
            routing.VehicleVar(index).SetValues([1,2,3,4,5])
    
    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(10)
      
    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    if assignment:
        print_solution(data, manager, routing, assignment)
    else:
        print('No solution found !')

if __name__ == '__main__':
    main()