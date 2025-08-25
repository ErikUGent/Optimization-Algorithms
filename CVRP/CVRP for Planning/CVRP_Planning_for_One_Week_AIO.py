# CVRP application for creating a planning for a VAR for one day for 5 vans with distance matrix calculation via Google Maps
# Jobs that need two workers are added to the same route

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import json
import GUI as GUI
from Distance_Matrix import *
from GUI import *
import tkinter as tk
from tkinter import ttk

def convert_time(min):
    hour = min // 60
    minutes = min % 60
    return "%02dh%02dm" % (hour, minutes) 

def jsonToData(file='JsonExport_MVDH.json', datasetName='MVdH_dataset'):
    with open(file, 'r') as f:
        datasetsdict = json.load(f)
    jsondata = datasetsdict[datasetName]
    
    return jsondata

data_j = jsonToData()

veh1_N = submit_veh1()
veh2_N = submit_veh2()
veh3_N = submit_veh3()
veh4_N = submit_veh4()
veh5_N = submit_veh5()
veh6_N = submit_veh6()

dist_matr = []
dist_matr = dist_matrix()
print(dist_matr)

def create_data_model():
    data = {}
    data['distance_matrix'] = dist_matr
    print(data['distance_matrix']) 
    data['demands'] = [x['Service'] for x in data_j]
    print(data['demands'])
    data['time_matrix'] = np.array(data['distance_matrix']) + data['demands']
    data['num_vehicles'] = 30
    data['num_nodes'] = len(data['demands'])
    data['depot'] = 0
    data['nodes'] = [x['Name'] for x in data_j]

    data['vehicle_capacities'] = []
    for i in range(data['num_vehicles']):
        data['veh_cap'] = data['vehicle_capacities'].append(480)
    
    data['starts'] = [int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh2_N), int(veh2_N), int(veh2_N), int(veh2_N), int(veh2_N), int(veh3_N), int(veh3_N), int(veh3_N), int(veh3_N), int(veh3_N), int(veh4_N), int(veh4_N), int(veh4_N), int(veh4_N), int(veh4_N), int(veh5_N), int(veh5_N), int(veh5_N), int(veh5_N), int(veh5_N), int(veh6_N), int(veh6_N), int(veh6_N), int(veh6_N), int(veh6_N)]
    data['ends'] = [int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh1_N), int(veh2_N), int(veh2_N), int(veh2_N), int(veh2_N), int(veh2_N), int(veh3_N), int(veh3_N), int(veh3_N), int(veh3_N), int(veh3_N), int(veh4_N), int(veh4_N), int(veh4_N), int(veh4_N), int(veh4_N), int(veh5_N), int(veh5_N), int(veh5_N), int(veh5_N), int(veh5_N), int(veh6_N), int(veh6_N), int(veh6_N), int(veh6_N), int(veh6_N)]
    
    data['2_workers'] = []
    for Customer in data_j:
        if Customer['Workers']==2:
            data['2_w'] = data['2_workers'].append(Customer['Name'])
    
    data['two_workers'] = []
    for node in data['2_workers']:
        data['two_w'] = data['two_workers'].append(data['nodes'].index(node))
    
    print(data['two_workers'])
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

    root = tk.Tk()
    root.geometry("1000x1000")
    root.title(" Planning Qurtinz ")
    Result_W = tk.Text(root, bg = "white", font = "Code 18")
    
    for vehicle_id in range(data['num_vehicles']):
        count = 1
        index = routing.Start(vehicle_id)
        plan_output = 'Route voor camionette {} - Starttijd 08h30:\n\n'.format(vehicle_id)
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
            
            if node_index == 0 or node_index == 1 or node_index == 2 :
                plan_output += 'Vertrek uit {0}: \n     Verplaatsing naar eerste plaatsing ({1}) \n     Eindtijd {3}e plaatsing ({2})\n'.format(node_name, node_time, route_total_start, count) 
            else:
                plan_output += '{0}: \n     Werktijd plaatsing ({1}) \n     Verplaatsing naar volgende plaatsing of depot ({2}) \n     Eindtijd {4}e plaatsing of aankomst depot ({3})\n'.format(node_name, node_load, node_time, route_total_start, count)
            count = count + 1    

        plan_output += 'Aankomst in {0}: {1}\n\n'.format(final_node_name,
                                                 route_distance)
        plan_output += 'Werk en Verplaatsing van camionette {0}: {1}\n'.format(vehicle_id, route_total)
        plan_output += 'Totale werktijd: {}\n'.format(route_load)
        plan_output += 'Totale reistijd: {}\n\n'.format(route_time)        
        print(plan_output)
        total_distance += route_distance_min
        total_load += route_load_min

        if route_load_min != 0:
            Result_W.insert(tk.END, plan_output)
            Result_W.insert(tk.END, '------------------------------------------------------------------------------------\n\n')
            Result_W.pack()
            
    print('Totale reistijd van alle routes: {}m'.format(total_distance))
    print('Totale werktijd van alle routes: {}'.format(total_load))

    Result_W.pack()
    Result_W.mainloop()

  
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

if __name__ == '__main__':
    main()