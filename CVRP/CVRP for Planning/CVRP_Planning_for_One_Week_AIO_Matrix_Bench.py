# CVRP application for creating a planning for a VAR for one week for 5 vans with a previously calaculated distance matrix
# Jobs that need two workers are added to the same route

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import json
import GUI as GUI
import tkinter as tk

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

def create_data_model():
    data = {}
    data['distance_matrix'] = [
 [ 0, 14, 21, 33, 17, 14, 11, 26, 22, 23, 28, 12,  8, 29, 18, 25, 22, 17,
  15, 32, 32, 32, 21, 22, 25, 23, 28,  8, 30, 29, 31, 30, 10, 34, 32, 39,
  44, 18, 16, 38, 42, 30, 31, 35, 25 ],
 [14,  0, 12, 19, 31, 22, 17, 23, 12, 24, 34, 12, 21, 42, 27, 36, 19, 31,
  28, 46, 21, 27,  7, 22, 29, 33, 19,  8, 16, 21, 33, 17,  6, 43, 31, 27,
  31, 30, 19, 43, 56, 44, 45, 34, 38 ],
 [21, 12,  0, 15, 37, 21, 28, 35, 22, 16, 28, 11, 25, 50, 38, 35,  9, 34,
  36, 51, 12, 15, 11, 34, 41, 43, 29, 19, 19,  9, 24, 23, 11, 39, 20, 19,
  24, 32, 15, 35, 62, 50, 48, 46, 39 ],
 [33, 19, 15,  0, 50, 36, 35, 35, 21, 31, 43, 25, 38, 61, 46, 51, 23, 48,
  47, 64,  8, 24, 12, 37, 46, 52, 25, 27,  9, 17, 37, 16, 23, 54, 32, 10,
  12, 47, 30, 49, 75, 63, 62, 47, 54 ],
 [17, 31, 37, 50,  0, 20, 21, 37, 38, 33, 31, 27, 13, 15, 18, 19, 35,  8,
   8, 15, 49, 45, 38, 31, 29, 18, 43, 24, 47, 44, 38, 46, 27, 31, 42, 56,
  61, 13, 27, 41, 25, 13, 16, 41, 15 ],
 [14, 22, 21, 36, 20,  0, 25, 40, 33, 12, 14, 11,  9, 35, 30, 15, 16, 15,
  23, 32, 33, 25, 27, 36, 39, 34, 40, 21, 37, 25, 18, 39, 16, 21, 21, 40,
  45, 11,  7, 24, 42, 33, 28, 49, 18 ],
 [11, 17, 28, 35, 21, 25,  0, 16, 18, 34, 40, 22, 18, 27, 10, 34, 32, 25,
  15, 35, 38, 41, 23, 11, 14, 17, 22,  9, 30, 37, 42, 27, 17, 45, 42, 44,
  47, 27, 27, 50, 44, 32, 37, 23, 33 ],
 [26, 23, 35, 35, 37, 40, 16,  0, 14, 46, 54, 33, 34, 40, 22, 51, 41, 41,
  30, 50, 40, 50, 26,  6, 14, 27, 11, 20, 26, 44, 55, 21, 27, 60, 53, 45,
  46, 44, 40, 64, 58, 47, 53, 12, 50 ],
 [22, 12, 22, 21, 38, 33, 18, 14,  0, 36, 46, 24, 30, 45, 28, 46, 30, 39,
  32, 52, 26, 37, 12, 16, 25, 34,  7, 14, 13, 30, 44,  9, 17, 54, 42, 31,
  33, 40, 30, 55, 62, 50, 53, 26, 47 ],
 [23, 24, 16, 31, 33, 12, 34, 46, 36,  0, 12, 13, 21, 48, 41, 23,  8, 27,
  35, 44, 25, 13, 26, 43, 48, 45, 43, 27, 35, 16,  8, 39, 19, 24,  9, 32,
  38, 23,  7, 19, 54, 45, 39, 56, 28 ],
 [28, 34, 28, 43, 31, 14, 40, 54, 46, 12,  0, 22, 23, 46, 44, 16, 20, 24,
  36, 39, 37, 24, 37, 50, 53, 47, 53, 34, 47, 28,  9, 50, 28, 12, 16, 43,
  49, 19, 15, 10, 48, 41, 32, 63, 22 ],
 [12, 12, 11, 25, 27, 11, 22, 33, 24, 13, 22,  0, 14, 40, 30, 26, 10, 23,
  26, 40, 23, 20, 16, 31, 36, 35, 31, 14, 26, 17, 21, 28,  6, 31, 21, 30,
  35, 21,  7, 31, 51, 40, 37, 44, 29 ],
 [ 8, 21, 25, 38, 13,  9, 18, 34, 30, 21, 23, 14,  0, 27, 21, 17, 23, 10,
  14, 26, 37, 33, 27, 29, 30, 25, 36, 16, 37, 31, 27, 37, 16, 27, 30, 44,
  49, 10, 14, 33, 37, 26, 24, 41, 17 ],
 [29, 42, 50, 61, 15, 35, 27, 40, 45, 48, 46, 40, 27,  0, 18, 32, 50, 22,
  14, 14, 62, 59, 49, 34, 27, 13, 48, 34, 57, 58, 53, 54, 39, 44, 57, 69,
  73, 27, 41, 55, 19,  9, 22, 39, 27 ],
 [18, 27, 38, 46, 18, 30, 10, 22, 28, 41, 44, 30, 21, 18,  0, 35, 40, 24,
  10, 29, 48, 50, 34, 16, 11,  6, 30, 19, 40, 46, 48, 37, 26, 47, 50, 54,
  58, 28, 34, 54, 37, 25, 33, 23, 32 ],
 [25, 36, 35, 51, 19, 15, 34, 51, 46, 23, 16, 26, 17, 32, 35,  0, 30, 11,
  25, 23, 47, 37, 41, 46, 46, 36, 53, 33, 51, 39, 25, 53, 30, 12, 30, 54,
  59,  7, 21, 23, 33, 26, 16, 57,  6 ],
 [22, 19,  9, 23, 35, 16, 32, 41, 30,  8, 20, 10, 23, 50, 40, 30,  0, 31,
  36, 48, 18, 10, 19, 39, 45, 45, 37, 23, 28,  9, 15, 32, 15, 32, 12, 24,
  30, 28,  9, 27, 59, 48, 44, 52, 34 ],
 [17, 31, 34, 48,  8, 15, 25, 41, 39, 27, 24, 23, 10, 22, 24, 11, 31,  0,
  14, 17, 46, 40, 37, 36, 35, 25, 45, 25, 47, 40, 31, 47, 25, 23, 35, 53,
  58,  5, 22, 33, 28, 18, 14, 47,  9 ],
 [15, 28, 36, 47,  8, 23, 15, 30, 32, 35, 36, 26, 14, 14, 10, 25, 36, 14,
   0, 20, 47, 46, 35, 24, 21, 11, 36, 20, 43, 44, 41, 41, 25, 37, 44, 54,
  58, 19, 28, 46, 30, 17, 23, 33, 22 ],
 [32, 46, 51, 64, 15, 32, 35, 50, 52, 44, 39, 40, 26, 14, 29, 23, 48, 17,
  20,  0, 63, 57, 53, 44, 39, 26, 57, 39, 62, 57, 47, 61, 41, 33, 52, 70,
  75, 21, 39, 46, 11,  5,  9, 52, 17 ],
 [32, 21, 12,  8, 49, 33, 38, 40, 26, 25, 37, 23, 37, 62, 48, 47, 18, 46,
  47, 63,  0, 17, 15, 41, 49, 54, 32, 29, 17, 10, 31, 23, 22, 49, 25,  7,
  13, 44, 26, 43, 74, 62, 60, 52, 51 ],
 [32, 27, 15, 24, 45, 25, 41, 50, 37, 13, 24, 20, 33, 59, 50, 37, 10, 40,
  46, 57, 17,  0, 25, 48, 55, 55, 44, 33, 31,  7, 16, 37, 24, 36,  9, 21,
  27, 36, 18, 27, 67, 58, 52, 61, 42 ],
 [21,  7, 11, 12, 38, 27, 23, 26, 12, 26, 37, 16, 27, 49, 34, 41, 19, 37,
  35, 53, 15, 25,  0, 26, 34, 40, 19, 15, 10, 18, 34, 13, 12, 47, 31, 21,
  24, 36, 22, 45, 63, 51, 51, 38, 44 ],
 [22, 22, 34, 37, 31, 36, 11,  6, 16, 43, 50, 31, 29, 34, 16, 46, 39, 36,
  24, 44, 41, 48, 26,  0,  9, 21, 16, 17, 29, 43, 52, 24, 25, 56, 51, 46,
  49, 38, 36, 60, 52, 40, 47, 13, 44 ],
 [25, 29, 41, 46, 29, 39, 14, 14, 25, 48, 53, 36, 30, 27, 11, 46, 45, 35,
  21, 39, 49, 55, 34,  9,  0, 14, 25, 22, 38, 50, 56, 34, 31, 57, 56, 55,
  58, 38, 41, 63, 46, 35, 44, 12, 43 ],
 [23, 33, 43, 52, 18, 34, 17, 27, 34, 45, 47, 35, 25, 13,  6, 36, 45, 25,
  11, 26, 54, 55, 40, 21, 14,  0, 36, 25, 46, 52, 52, 43, 32, 48, 54, 60,
  64, 30, 38, 57, 32, 21, 31, 26, 33 ],
 [28, 19, 29, 25, 43, 40, 22, 11,  7, 43, 53, 31, 36, 48, 30, 53, 37, 45,
  36, 57, 32, 44, 19, 16, 25, 36,  0, 20, 16, 37, 51, 10, 25, 61, 49, 35,
  36, 46, 38, 62, 66, 54, 58, 22, 53 ],
 [ 8,  8, 19, 27, 24, 21,  9, 20, 14, 27, 34, 14, 16, 34, 19, 33, 23, 25,
  20, 39, 29, 33, 15, 17, 22, 25, 20,  0, 23, 28, 35, 22,  8, 41, 34, 35,
  39, 26, 20, 44, 49, 37, 39, 30, 33 ],
 [30, 16, 19,  9, 47, 37, 30, 26, 13, 35, 47, 26, 37, 57, 40, 51, 28, 47,
  43, 62, 17, 31, 10, 29, 38, 46, 16, 23,  0, 24, 43,  6, 22, 57, 38, 19,
  20, 46, 32, 54, 72, 60, 61, 38, 54 ],
 [29, 21,  9, 17, 44, 25, 37, 44, 30, 16, 28, 17, 31, 58, 46, 39,  9, 40,
  44, 57, 10,  7, 18, 43, 50, 52, 37, 28, 24,  0, 21, 30, 20, 40, 15, 16,
  22, 37, 18, 33, 68, 57, 53, 55, 43 ],
 [31, 33, 24, 37, 38, 18, 42, 55, 44,  8,  9, 21, 27, 53, 48, 25, 15, 31,
  41, 47, 31, 16, 34, 52, 56, 52, 51, 35, 43, 21,  0, 47, 28, 21,  7, 36,
  42, 26, 15, 12, 57, 49, 41, 65, 30 ],
 [30, 17, 23, 16, 46, 39, 27, 21,  9, 39, 50, 28, 37, 54, 37, 53, 32, 47,
  41, 61, 23, 37, 13, 24, 34, 43, 10, 22,  6, 30, 47,  0, 23, 60, 43, 26,
  26, 47, 35, 58, 71, 59, 61, 32, 54 ],
 [10,  6, 11, 23, 27, 16, 17, 27, 17, 19, 28,  6, 16, 39, 26, 30, 15, 25,
  25, 41, 22, 24, 12, 25, 31, 32, 25,  8, 22, 20, 28, 23,  0, 37, 26, 29,
  34, 25, 13, 37, 52, 40, 40, 38, 32 ],
 [34, 43, 39, 54, 31, 21, 45, 60, 54, 24, 12, 31, 27, 44, 47, 12, 32, 23,
  37, 33, 49, 36, 47, 56, 57, 48, 61, 41, 57, 40, 21, 60, 37,  0, 27, 55,
  61, 18, 25, 14, 41, 37, 25, 68, 17 ],
 [32, 31, 20, 32, 42, 21, 42, 53, 42,  9, 16, 21, 30, 57, 50, 30, 12, 35,
  44, 52, 25,  9, 31, 51, 56, 54, 49, 34, 38, 15,  7, 43, 26, 27,  0, 30,
  36, 31, 16, 18, 62, 53, 46, 64, 36 ],
 [39, 27, 19, 10, 56, 40, 44, 45, 31, 32, 43, 30, 44, 69, 54, 54, 24, 53,
  54, 70,  7, 21, 21, 46, 55, 60, 35, 35, 19, 16, 36, 26, 29, 55, 30,  0,
   6, 51, 33, 48, 81, 69, 67, 57, 58 ],
 [44, 31, 24, 12, 61, 45, 47, 46, 33, 38, 49, 35, 49, 73, 58, 59, 30, 58,
  58, 75, 13, 27, 24, 49, 58, 64, 36, 39, 20, 22, 42, 26, 34, 61, 36,  6,
   0, 56, 38, 54, 86, 74, 72, 58, 63 ],
 [18, 30, 32, 47, 13, 11, 27, 44, 40, 23, 19, 21, 10, 27, 28,  7, 28,  5,
  19, 21, 44, 36, 36, 38, 38, 30, 46, 26, 46, 37, 26, 47, 25, 18, 31, 51,
  56,  0, 18, 28, 31, 23, 16, 50,  7 ],
 [16, 19, 15, 30, 27,  7, 27, 40, 30,  7, 15,  7, 14, 41, 34, 21,  9, 22,
  28, 39, 26, 18, 22, 36, 41, 38, 38, 20, 32, 18, 15, 35, 13, 25, 16, 33,
  38, 18,  0, 24, 49, 39, 35, 49, 25 ],
 [38, 43, 35, 49, 41, 24, 50, 64, 55, 19, 10, 31, 33, 55, 54, 23, 27, 33,
  46, 46, 43, 27, 45, 60, 63, 57, 62, 44, 54, 33, 12, 58, 37, 14, 18, 48,
  54, 28, 24,  0, 55, 49, 38, 73, 29 ],
 [42, 56, 62, 75, 25, 42, 44, 58, 62, 54, 48, 51, 37, 19, 37, 33, 59, 28,
  30, 11, 74, 67, 63, 52, 46, 32, 66, 49, 72, 68, 57, 71, 52, 41, 62, 81,
  86, 31, 49, 55,  0, 12, 16, 58, 27 ],
 [30, 44, 50, 63, 13, 33, 32, 47, 50, 45, 41, 40, 26,  9, 25, 26, 48, 18,
  17,  5, 62, 58, 51, 40, 35, 21, 54, 37, 60, 57, 49, 59, 40, 37, 53, 69,
  74, 23, 39, 49, 12,  0, 13, 47, 20 ],
 [31, 45, 48, 62, 16, 28, 37, 53, 53, 39, 32, 37, 24, 22, 33, 16, 44, 14,
  23,  9, 60, 52, 51, 47, 44, 31, 58, 39, 61, 53, 41, 61, 40, 25, 46, 67,
  72, 16, 35, 38, 16, 13,  0, 56, 10 ],
 [35, 34, 46, 47, 41, 49, 23, 12, 26, 56, 63, 44, 41, 39, 23, 57, 52, 47,
  33, 52, 52, 61, 38, 13, 12, 26, 22, 30, 38, 55, 65, 32, 38, 68, 64, 57,
  58, 50, 49, 73, 58, 47, 56,  0, 55 ],
 [25, 38, 39, 54, 15, 18, 33, 50, 47, 28, 22, 29, 17, 27, 32,  6, 34,  9,
  22, 17, 51, 42, 44, 44, 43, 33, 53, 33, 54, 43, 30, 54, 32, 17, 36, 58,
  63,  7, 25, 29, 27, 20, 10, 55,  0 ]]


    data['demands'] = [0, 7, 30, 16, 9, 21, 15, 19, 23, 11, 5, 19, 29, 23, 21, 10, 15, 3, 41, 9, 28, 8, 8, 16, 10, 28, 7, 15, 14, 6, 19, 11, 12, 23, 26, 17, 6, 9, 15, 14, 7, 27, 13, 11, 16]
    print(data['demands'])
    data['time_matrix'] = data['distance_matrix']
    data['num_vehicles'] = 6
    data['num_nodes'] = len(data['demands'])
    data['depot'] = 0
    data['nodes'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]

    data['vehicle_capacities'] = []
    for i in range(data['num_vehicles']):
        data['veh_cap'] = data['vehicle_capacities'].append(150)
    
    data['starts'] = [0, 0, 0, 0, 0, 0]
    data['ends'] = [0, 0, 0, 0, 0, 0]

    data['two_workers'] = [4, 6, 19, 23, 26, 38, 14, 44]
    
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
            
    print('Total Distance of all routes: {}m'.format(total_distance))
    print('Total Load of all routes: {}'.format(total_load))

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
        510,  # vehicle maximum time of route
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

    for node in range(1, len(data['time_matrix'])):
        if node in (data['two_workers']):
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