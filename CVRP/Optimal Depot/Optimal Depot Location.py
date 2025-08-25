from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import pandas as pd

import time
start_time = time.time()

def convert_time(min):
    hour = min // 60
    minutes = min % 60
    return "%02dh%02dm" % (hour, minutes) 

veh1_N = 0
X_Cord_Max= [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
Y_Cord_Max= [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
final_result = []
depot_coord = []

def dist_matrix():
    data = [[k, l], [27, 39], [39, 29], [32, 34], [20, 26], [40, 30], [21, 37], [17, 33], [31, 22], [9, 33], [28, 21], [32, 27], [31, 32], [5, 25], [12, 32], [36, 16], [22, 1], [27, 23], [17, 33], [13, 13], [27, 38], [32, 12], [32, 7], [16, 27], [8, 32], [7, 28], [27, 31], [30, 18], [23, 37], [38, 28], [18, 27], [17, 39], [32, 26], [36, 10], [11, 33], [22, 33], [13, 19], [32, 22], [25, 35], [32, 15], [5, 6], [10, 17], [21, 10], [5, 34], [30, 15]]
    df = pd.DataFrame(data, columns=['xcord', 'ycord'], dtype='int16')
    n_df=(df.values)

    (df.values).shape

    matrix=np.zeros(((df.values).shape[0],(df.values).shape[0]))

    for i in range((df.values).shape[0]):
        for j in range((df.values).shape[0]):
            matrix[i,j]=round(float(np.sqrt(np.sum((n_df[i]-n_df[j])**2))), 0)

    np.set_printoptions(threshold=np.inf)
    return matrix

def create_data_model():
    data = {}
    data['distance_matrix'] = dist_matrix()
    data['demands'] = [0,20,30,50,70,20,60,15,40,85,90,20,45,80,30,45,70,30,60,25,35,85,90,30,15,40,30,55,70,35,60,75,40,85,90,35,10,20,30,10,70,30,15,50,85]
    data['time_matrix'] = np.array(data['distance_matrix']) + data['demands']
    data['num_vehicles'] = 30
    data['num_nodes'] = len(data['demands'])
    data['depot'] = 0
    data['nodes'] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44]

    data['vehicle_capacities'] = []
    for i in range(data['num_vehicles']):
        data['veh_cap'] = data['vehicle_capacities'].append(480)
    
    data['starts'] = [int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N)]
    data['ends'] = [int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N)]
    
    data['two_workers'] = [1,7,9,17,23,29,34,38]
  
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
        count = 1
        index = routing.Start(vehicle_id)
        route_distance_min = 510
        route_time_min = 0
        route_load_min = 0
        final_node_index = manager.IndexToNode(index)
        final_node_name = data['nodes'][final_node_index]
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            from_node = manager.IndexToNode(node_index)
            to_index = assignment.Value(routing.NextVar(index))
            to_node = manager.IndexToNode(to_index)
            node_name = data['nodes'][node_index]
            node_load_min = data['demands'][node_index]
            node_load = convert_time(node_load_min)
            node_time_min = data['distance_matrix'][from_node][to_node]
            node_time = convert_time(node_time_min)
            route_load_min += data['demands'][node_index]
            route_load = convert_time(route_load_min)
            route_time_min += data['distance_matrix'][from_node][to_node]
            route_time = convert_time(route_time_min)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance_min += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
            route_distance = convert_time(route_distance_min)
            route_total_min = route_distance_min - 510
            route_total = convert_time(route_total_min)

            route_total_start_min = route_distance_min
            route_total_start = convert_time(route_total_start_min)
    
        total_distance += route_distance_min
        total_load += route_load_min
 
    print('Totale afstand van alle routes: {}m'.format(total_distance))
    print('Totale load van alle routes: {}'.format(total_load))
    final_result.append(total_distance)
  
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

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Allow all locations except the first two to be droppable.
    disjunction_penalty = 0
    for node in range(1, len(data['time_matrix'])):
      routing.AddDisjunction([manager.NodeToIndex(node)], disjunction_penalty)
    
    # Assign jobs for two workers to the same vehicle
    for node in range(1, len(data['time_matrix'])):
        if node in (data['two_workers']):
            index =  manager.NodeToIndex(node)
            routing.VehicleVar(index).SetValues([0,1,2,3])
        else:
            index =  manager.NodeToIndex(node)
            routing.VehicleVar(index).SetValues([4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])

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

for index1 in range(0, len(X_Cord_Max)):
    for index2 in range(0, len(Y_Cord_Max)):
        k= X_Cord_Max[index1]
        l= Y_Cord_Max[index2]
        depot_coord.append([k,l])
        if __name__ == '__main__':
            main()

final_result_Min = min(final_result)
ind_fin_res=final_result.index(final_result_Min)
print(final_result_Min)
print(ind_fin_res)
print(depot_coord)
print(depot_coord[ind_fin_res])
print('the elapsed time:%s'% (round(time.time() - start_time, 4)))