# CVRP application for creating a planning for a VAR for one day for 5 vans with a previously calaculated distance matrix
# Jobs that need two workers are added to the same route
# Time windows are included

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import json
import GUI as GUI
from GUI import *
import tkinter as tk

def merge(list1, list2):
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
     
    return merged_list

def convert_time(min):
    hour = min // 60
    minutes = min % 60
    return "%02dh%02dm" % (hour, minutes) 

def jsonToData(file='JsonExport.json', datasetName='Qurtinz_dataset'):
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

def create_data_model():
    data = {}
    data['distance_matrix'] = [
    [0, 54, 22, 51, 72, 36, 26, 52, 26, 57, 23, 17, 38, 45, 29, 48, 65, 74, 76, 88, 51, 53, 40, 47, 50, 54, 80, 59, 40, 91, 52, 73, 24, 55, 62, 49, 54, 22, 51, 14, 56, 14], 
    [54, 0, 40, 69, 108, 37, 59, 76, 50, 93, 43, 54, 58, 81, 69, 84, 46, 55, 96, 108, 11, 89, 66, 83, 86, 92, 100, 7, 36, 125, 90, 54, 45, 75, 78, 85, 35, 42, 86, 65, 92, 53], 
    [21, 40, 0, 44, 82, 19, 32, 50, 28, 67, 17, 25, 32, 55, 47, 57, 51, 60, 70, 81, 38, 62, 39, 56, 59, 66, 74, 45, 33, 98, 64, 60, 18, 49, 56, 59, 40, 16, 60, 32, 66, 23], 
    [51, 70, 44, 0, 99, 45, 49, 54, 63, 69, 42, 46, 33, 72, 68, 75, 83, 92, 71, 83, 70, 74, 56, 72, 76, 83, 75, 74, 43, 100, 81, 92, 43, 50, 49, 76, 72, 40, 77, 56, 71, 45], 
    [71, 110, 82, 100, 0, 85, 72, 73, 80, 53, 79, 79, 78, 43, 78, 41, 121, 130, 72, 89, 107, 49, 53, 40, 40, 34, 81, 115, 90, 82, 32, 129, 81, 63, 81, 42, 110, 78, 38, 66, 53, 74], 
    [37, 38, 19, 45, 85, 0, 36, 53, 42, 70, 20, 30, 35, 58, 55, 60, 60, 70, 73, 85, 40, 65, 42, 59, 62, 69, 77, 43, 17, 102, 67, 69, 18, 52, 59, 62, 50, 24, 63, 43, 69, 30], 
    [24, 56, 28, 46, 72, 32, 0, 40, 39, 57, 26, 20, 33, 45, 34, 47, 67, 76, 71, 83, 54, 52, 29, 46, 49, 56, 75, 61, 37, 91, 54, 76, 27, 50, 57, 49, 56, 24, 50, 23, 56, 14], 
    [52, 77, 49, 52, 72, 55, 42, 0, 68, 51, 46, 49, 25, 45, 66, 48, 87, 97, 54, 66, 74, 51, 29, 46, 49, 56, 58, 82, 60, 83, 54, 96, 47, 32, 46, 49, 77, 45, 50, 54, 44, 43], 
    [25, 48, 26, 60, 83, 40, 39, 66, 0, 68, 32, 31, 47, 56, 32, 59, 58, 68, 85, 97, 45, 63, 51, 57, 60, 65, 89, 53, 49, 102, 63, 67, 34, 65, 72, 60, 48, 31, 61, 25, 67, 30], 
    [57, 93, 65, 67, 51, 69, 56, 51, 67, 0, 62, 63, 41, 27, 64, 22, 104, 113, 35, 52, 90, 14, 36, 19, 28, 34, 44, 98, 74, 67, 33, 112, 64, 26, 45, 28, 93, 61, 29, 53, 28, 57], 
    [23, 45, 17, 40, 77, 19, 28, 45, 35, 62, 0, 22, 27, 50, 47, 53, 55, 65, 65, 77, 42, 58, 35, 52, 55, 61, 69, 50, 28, 94, 59, 64, 7, 44, 51, 54, 45, 6, 55, 34, 61, 23], 
    [16, 52, 23, 49, 78, 27, 21, 45, 33, 62, 21, 0, 36, 50, 38, 53, 62, 72, 74, 86, 49, 58, 35, 52, 55, 61, 78, 57, 32, 96, 60, 71, 22, 53, 60, 54, 52, 16, 56, 26, 61, 7], 
    [36, 58, 30, 32, 77, 37, 34, 25, 48, 43, 27, 31, 0, 51, 53, 49, 68, 78, 45, 57, 55, 48, 41, 46, 54, 61, 49, 63, 42, 74, 59, 77, 28, 24, 31, 54, 57, 26, 55, 42, 44, 30], 
    [44, 80, 52, 70, 42, 55, 42, 43, 53, 28, 49, 50, 50, 0, 51, 16, 91, 100, 46, 63, 77, 23, 23, 15, 9, 26, 55, 85, 60, 61, 24, 99, 51, 37, 54, 18, 80, 48, 13, 40, 25, 44], 
    [27, 68, 46, 68, 80, 54, 35, 64, 31, 65, 46, 38, 55, 53, 0, 56, 79, 89, 84, 101, 66, 61, 48, 55, 57, 62, 93, 73, 59, 99, 60, 88, 48, 72, 79, 57, 69, 45, 58, 17, 64, 32], 
    [50, 86, 57, 75, 39, 61, 48, 48, 59, 24, 55, 55, 49, 16, 57, 0, 96, 106, 43, 60, 83, 16, 28, 5, 11, 23, 52, 90, 66, 58, 21, 105, 56, 34, 53, 12, 85, 53, 17, 45, 24, 49], 
    [66, 46, 52, 83, 121, 60, 71, 88, 62, 106, 56, 67, 70, 94, 82, 96, 0, 26, 108, 120, 43, 101, 78, 95, 98, 105, 112, 51, 71, 137, 103, 19, 57, 88, 95, 98, 30, 54, 99, 77, 104, 66], 
    [76, 56, 62, 93, 131, 70, 81, 98, 72, 116, 66, 77, 80, 104, 92, 106, 28, 0, 118, 130, 53, 111, 88, 105, 108, 115, 122, 56, 65, 147, 113, 21, 67, 98, 105, 108, 43, 64, 109, 87, 114, 76], 
    [74, 96, 68, 70, 70, 75, 72, 56, 86, 36, 65, 69, 44, 46, 84, 42, 106, 116, 0, 26, 93, 41, 56, 39, 48, 54, 26, 101, 80, 43, 52, 115, 66, 29, 48, 47, 96, 64, 48, 73, 48, 68], 
    [85, 107, 79, 82, 86, 86, 84, 68, 98, 52, 77, 81, 55, 62, 100, 58, 118, 127, 28, 0, 105, 57, 69, 55, 63, 70, 18, 112, 91, 41, 68, 127, 78, 40, 59, 63, 107, 75, 64, 88, 62, 80], 
    [52, 11, 38, 69, 106, 40, 57, 74, 48, 91, 41, 52, 56, 79, 67, 82, 44, 53, 94, 106, 0, 87, 64, 81, 84, 90, 98, 14, 39, 123, 88, 52, 43, 73, 80, 83, 33, 40, 84, 63, 90, 51], 
    [54, 90, 62, 74, 47, 65, 52, 50, 63, 14, 59, 59, 47, 23, 61, 16, 100, 110, 42, 59, 87, 0, 33, 15, 24, 31, 51, 95, 70, 66, 29, 109, 60, 33, 51, 21, 90, 58, 25, 49, 22, 53], 
    [38, 65, 37, 56, 52, 41, 28, 28, 50, 37, 35, 35, 43, 25, 48, 28, 76, 85, 56, 71, 63, 32, 0, 26, 29, 36, 63, 70, 46, 71, 34, 85, 36, 38, 53, 29, 65, 33, 30, 37, 36, 29], 
    [50, 86, 57, 72, 39, 61, 48, 48, 59, 21, 55, 55, 46, 17, 57, 4, 96, 106, 40, 57, 83, 15, 28, 0, 15, 23, 49, 90, 66, 58, 21, 105, 56, 31, 50, 14, 85, 54, 17, 45, 21, 49], 
    [50, 86, 58, 76, 42, 61, 48, 49, 59, 28, 55, 55, 52, 11, 57, 11, 96, 106, 47, 64, 83, 24, 29, 14, 0, 25, 56, 91, 66, 60, 24, 105, 56, 37, 56, 16, 86, 54, 19, 46, 28, 49], 
    [47, 91, 63, 82, 35, 67, 54, 54, 57, 34, 60, 60, 59, 24, 55, 22, 102, 111, 53, 70, 89, 30, 34, 21, 22, 0, 62, 96, 72, 63, 5, 111, 62, 44, 63, 23, 91, 59, 18, 43, 34, 54], 
    [80, 101, 73, 76, 80, 80, 78, 62, 92, 46, 71, 75, 49, 56, 94, 52, 112, 121, 26, 18, 99, 51, 63, 49, 57, 64, 0, 106, 85, 49, 62, 121, 72, 34, 53, 57, 101, 69, 58, 82, 56, 74], 
    [59, 7, 46, 72, 114, 42, 65, 82, 57, 99, 49, 60, 64, 87, 74, 90, 52, 56, 102, 114, 14, 94, 71, 88, 91, 98, 106, 0, 39, 130, 96, 61, 50, 81, 81, 91, 41, 48, 92, 70, 98, 59], 
    [44, 36, 36, 47, 94, 20, 45, 62, 56, 79, 34, 39, 45, 67, 64, 70, 73, 68, 83, 94, 40, 75, 52, 69, 72, 78, 87, 40, 0, 111, 76, 81, 30, 62, 69, 71, 62, 34, 72, 53, 78, 39], 
    [92, 126, 97, 100, 80, 104, 91, 86, 102, 68, 95, 98, 74, 62, 100, 60, 136, 146, 43, 41, 123, 66, 71, 58, 60, 64, 49, 130, 109, 0, 62, 145, 96, 59, 77, 55, 125, 94, 58, 88, 72, 92], 
    [49, 89, 61, 80, 33, 65, 52, 52, 58, 33, 59, 59, 57, 22, 56, 21, 100, 109, 51, 68, 87, 28, 32, 19, 20, 4, 60, 94, 70, 61, 0, 109, 60, 42, 61, 21, 89, 57, 16, 44, 33, 53], 
    [75, 55, 61, 92, 130, 69, 80, 97, 71, 114, 65, 75, 79, 102, 91, 105, 17, 21, 117, 129, 52, 110, 87, 104, 107, 113, 121, 60, 78, 146, 112, 0, 66, 96, 103, 106, 42, 63, 108, 86, 113, 75], 
    [24, 46, 18, 42, 79, 18, 30, 47, 37, 64, 8, 24, 29, 52, 49, 54, 57, 67, 67, 78, 44, 59, 36, 53, 56, 63, 71, 51, 25, 95, 61, 66, 0, 46, 53, 56, 46, 9, 57, 35, 63, 24], 
    [53, 75, 47, 50, 62, 54, 52, 34, 66, 28, 44, 49, 23, 37, 71, 34, 86, 95, 30, 42, 73, 33, 37, 31, 39, 46, 34, 80, 59, 59, 44, 95, 46, 0, 27, 39, 75, 43, 40, 59, 30, 48], 
    [62, 78, 56, 46, 81, 63, 60, 45, 74, 47, 53, 58, 32, 55, 79, 53, 94, 104, 49, 61, 80, 52, 55, 50, 58, 65, 53, 82, 68, 78, 63, 103, 54, 28, 0, 58, 84, 52, 59, 68, 48, 56], 
    [51, 87, 59, 78, 40, 63, 50, 50, 61, 31, 56, 57, 55, 19, 58, 13, 98, 107, 49, 66, 85, 23, 30, 14, 16, 24, 58, 92, 68, 55, 22, 107, 58, 40, 59, 0, 87, 55, 19, 47, 30, 51], 
    [54, 34, 41, 71, 109, 48, 59, 77, 50, 94, 44, 55, 58, 82, 70, 84, 29, 41, 96, 108, 32, 89, 66, 83, 86, 93, 101, 39, 59, 125, 91, 40, 45, 76, 83, 86, 0, 43, 87, 65, 93, 54], 
    [20, 44, 16, 39, 76, 23, 27, 44, 32, 61, 6, 17, 26, 49, 45, 52, 54, 64, 64, 76, 41, 57, 34, 51, 54, 60, 68, 49, 28, 93, 58, 63, 9, 43, 50, 53, 44, 0, 54, 31, 60, 18], 
    [50, 86, 58, 76, 37, 61, 48, 49, 59, 29, 55, 56, 54, 9, 57, 17, 97, 106, 48, 65, 83, 25, 29, 16, 16, 17, 57, 91, 66, 58, 15, 105, 57, 39, 58, 18, 86, 54, 0, 46, 29, 50], 
    [15, 65, 33, 58, 71, 44, 25, 54, 24, 56, 34, 28, 45, 44, 19, 47, 76, 85, 75, 91, 62, 51, 39, 45, 48, 53, 84, 70, 49, 90, 51, 84, 35, 62, 69, 48, 65, 32, 49, 0, 55, 22], 
    [56, 92, 64, 69, 52, 68, 55, 43, 65, 29, 61, 62, 42, 26, 63, 25, 103, 112, 47, 64, 90, 22, 34, 21, 29, 36, 56, 97, 73, 71, 34, 111, 63, 31, 46, 29, 92, 60, 30, 52, 0, 56], 
    [13, 55, 25, 44, 73, 30, 15, 41, 33, 58, 24, 8, 31, 46, 33, 48, 66, 75, 69, 81, 52, 53, 30, 47, 50, 57, 73, 60, 35, 92, 55, 74, 26, 48, 55, 50, 55, 19, 51, 21, 57, 0]
    ]
    data['demands'] = [x['Service'] for x in data_j]
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
    
    data['interv_start'] = [x['Start'] for x in data_j]
    data['interv_end'] = [x['End'] for x in data_j]
    
    data['time_windows'] = merge(data['interv_start'], data['interv_end'])
    
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
        510,  # null capacity slack
        510,  # vehicle maximum time of route
        True,  # start cumul to zero
        'Time',)

    time_dimension = routing.GetDimensionOrDie('Time')
    
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i))
        )
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))
    
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
    disjunction_penalty = 200
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