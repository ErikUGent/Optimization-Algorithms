
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():

    data = {}
    data['distance_matrix'] = [
 [0.0000e+00, 4.5150e+01, 4.4980e+01, 4.4630e+01, 4.4270e+01, 4.4030e+01,
  4.3790e+01, 4.3240e+01, 4.2830e+01, 4.6490e+01, 4.5580e+01, 6.7560e+02,
  6.7469e+02, 6.7380e+02, 2.2392e+02, 2.2354e+02, 2.2287e+02],
 [4.5150e+01, 0.0000e+00, 7.4000e-01, 1.3700e+00, 2.0200e+00, 2.7100e+00,
  3.7400e+00, 4.1300e+00, 4.4700e+00, 2.0200e+00, 1.0800e+00, 6.3120e+02,
  6.3034e+02, 6.2949e+02, 1.9841e+02, 1.9763e+02, 1.9666e+02],
 [4.4980e+01, 7.4000e-01, 0.0000e+00, 6.5000e-01, 1.3100e+00, 1.9900e+00,
  3.0100e+00, 3.4300e+00, 3.7800e+00, 2.7000e+00, 1.8200e+00, 6.3152e+02,
  6.3065e+02, 6.2980e+02, 1.9913e+02, 1.9834e+02, 1.9737e+02],
 [4.4630e+01, 1.3700e+00, 6.5000e-01, 0.0000e+00, 6.7000e-01, 1.3500e+00,
  2.3700e+00, 2.7800e+00, 3.1300e+00, 3.3400e+00, 2.4500e+00, 6.3197e+02,
  6.3111e+02, 6.3027e+02, 1.9977e+02, 1.9899e+02, 1.9801e+02],
 [4.4270e+01, 2.0200e+00, 1.3100e+00, 6.7000e-01, 0.0000e+00, 6.9000e-01,
  1.7200e+00, 2.1100e+00, 2.4700e+00, 4.0100e+00, 3.1100e+00, 6.3245e+02,
  6.3159e+02, 6.3075e+02, 2.0043e+02, 1.9965e+02, 1.9868e+02],
 [4.4030e+01, 2.7100e+00, 1.9900e+00, 1.3500e+00, 6.9000e-01, 0.0000e+00,
  1.0400e+00, 1.4400e+00, 1.8200e+00, 4.6900e+00, 3.7900e+00, 6.3283e+02,
  6.3198e+02, 6.3114e+02, 2.0112e+02, 2.0033e+02, 1.9936e+02],
 [4.3790e+01, 3.7400e+00, 3.0100e+00, 2.3700e+00, 1.7200e+00, 1.0400e+00,
  0.0000e+00, 5.8000e-01, 1.0300e+00, 5.6900e+00, 4.8200e+00, 6.3332e+02,
  6.3247e+02, 6.3164e+02, 2.0213e+02, 2.0134e+02, 2.0037e+02],
 [4.3240e+01, 4.1300e+00, 3.4300e+00, 2.7800e+00, 2.1100e+00, 1.4400e+00,
  5.8000e-01, 0.0000e+00, 4.4000e-01, 6.1200e+00, 5.2100e+00, 6.3391e+02,
  6.3305e+02, 6.3222e+02, 2.0254e+02, 2.0176e+02, 2.0079e+02],
 [4.2830e+01, 4.4700e+00, 3.7800e+00, 3.1300e+00, 2.4700e+00, 1.8200e+00,
  1.0300e+00, 4.4000e-01, 0.0000e+00, 6.4700e+00, 5.5300e+00, 6.3435e+02,
  6.3350e+02, 6.3266e+02, 2.0287e+02, 2.0209e+02, 2.0112e+02],
 [4.6490e+01, 2.0200e+00, 2.7000e+00, 3.3400e+00, 4.0100e+00, 4.6900e+00,
  5.6900e+00, 6.1200e+00, 6.4700e+00, 0.0000e+00, 1.0400e+00, 6.2963e+02,
  6.2875e+02, 6.2790e+02, 1.9644e+02, 1.9565e+02, 1.9467e+02],
 [4.5580e+01, 1.0800e+00, 1.8200e+00, 2.4500e+00, 3.1100e+00, 3.7900e+00,
  4.8200e+00, 5.2100e+00, 5.5300e+00, 1.0400e+00, 0.0000e+00, 6.3061e+02,
  6.2974e+02, 6.2888e+02, 1.9733e+02, 1.9655e+02, 1.9558e+02],
 [6.7560e+02, 6.3120e+02, 6.3152e+02, 6.3197e+02, 6.3245e+02, 6.3283e+02,
  6.3332e+02, 6.3391e+02, 6.3435e+02, 6.2963e+02, 6.3061e+02, 0.0000e+00,
  3.2000e+00, 6.2700e+00, 5.2584e+02, 5.2415e+02, 5.2304e+02],
 [6.7469e+02, 6.3034e+02, 6.3065e+02, 6.3111e+02, 6.3159e+02, 6.3198e+02,
  6.3247e+02, 6.3305e+02, 6.3350e+02, 6.2875e+02, 6.2974e+02, 3.2000e+00,
  0.0000e+00, 3.0700e+00, 5.2411e+02, 5.2244e+02, 5.2134e+02],
 [6.7380e+02, 6.2949e+02, 6.2980e+02, 6.3027e+02, 6.3075e+02, 6.3114e+02,
  6.3164e+02, 6.3222e+02, 6.3266e+02, 6.2790e+02, 6.2888e+02, 6.2700e+00,
  3.0700e+00, 0.0000e+00, 5.2245e+02, 5.2079e+02, 5.1969e+02],
 [2.2392e+02, 1.9841e+02, 1.9913e+02, 1.9977e+02, 2.0043e+02, 2.0112e+02,
  2.0213e+02, 2.0254e+02, 2.0287e+02, 1.9644e+02, 1.9733e+02, 5.2584e+02,
  5.2411e+02, 5.2245e+02, 0.0000e+00, 2.3200e+00, 4.2200e+00],
 [2.2354e+02, 1.9763e+02, 1.9834e+02, 1.9899e+02, 1.9965e+02, 2.0033e+02,
  2.0134e+02, 2.0176e+02, 2.0209e+02, 1.9565e+02, 1.9655e+02, 5.2415e+02,
  5.2244e+02, 5.2079e+02, 2.3200e+00, 0.0000e+00, 1.9300e+00],
 [2.2287e+02, 1.9666e+02, 1.9737e+02, 1.9801e+02, 1.9868e+02, 1.9936e+02,
  2.0037e+02, 2.0079e+02, 2.0112e+02, 1.9467e+02, 1.9558e+02, 5.2304e+02,
  5.2134e+02, 5.1969e+02, 4.2200e+00, 1.9300e+00, 0.0000e+00],
    ]  
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def print_solution(manager, routing, solution):
    print('Objective: {} kilometers'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)

def main():
    data = create_data_model()

    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        # Returns the distance between the two nodes.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(manager, routing, solution)

if __name__ == '__main__':
    main()
