from curses import A_LEFT
from networkx import DiGraph, from_numpy_matrix, relabel_nodes, set_node_attributes
from numpy import array
from vrpy import VehicleRoutingProblem
import networkx as nx
import time

start_time = time.time()

def compose (f, g):
    return lambda x : f(g)

# Distance matrix

DISTANCES = [
 [ 0,  45,  45,  45,  44,  44,  44,  43,  43,  46,  46, 676, 675, 674, 224, 224, 223, 0],
 [ 0,   0,   1,   1,   2,   3,   4,   4,   4,   2,   1, 631, 630, 629, 198, 198, 197, 45],
 [ 0,   1,   0,   1,   1,   2,   3,   3,   4,   3,   2, 632, 631, 630, 199, 198, 197, 45],
 [ 0,   1,   1,   0,   1,   1,   2,   3,   3,   3,   2, 632, 631, 630, 200, 199, 198, 45],
 [ 0,   2,   1,   1,   0,   1,   2,   2,   2,   4,   3, 632, 632, 631, 200, 200, 199, 44],
 [ 0,   3,   2,   1,   1,   0,   1,   1,   2,   5,   4, 633, 632, 631, 201, 200, 199, 44],
 [ 0,   4,   3,   2,   2,   1,   0,   1,   1,   6,   5, 633, 632, 632, 202, 201, 200, 44],
 [ 0,   4,   3,   3,   2,   1,   1,   0,   0,   6,   5, 634, 633, 632, 203, 202, 201, 43],
 [ 0,   4,   4,   3,   2,   2,   1,   0,   0,   6,   6, 634, 633, 633, 203, 202, 201, 43],
 [ 0,   2,   3,   3,   4,   5,   6,   6,   6,   0,   1, 630, 629, 628, 196, 196, 195, 46],
 [ 0,   1,   2,   2,   3,   4,   5,   5,   6,   1,   0, 631, 630, 629, 197, 197, 196, 46],
 [ 0, 631, 632, 632, 632, 633, 633, 634, 634, 630, 631,   0,   3,   6, 526, 524, 523, 676],
 [ 0, 630, 631, 631, 632, 632, 632, 633, 633, 629, 630,   3,   0,   3, 524, 522, 521, 675],
 [ 0, 629, 630, 630, 631, 631, 632, 632, 633, 628, 629,   6,   3,   0, 522, 521, 520, 674],
 [ 0, 198, 199, 200, 200, 201, 202, 203, 203, 196, 197, 526, 524, 522,   0,   2,   4, 224],
 [ 0, 198, 198, 199, 200, 200, 201, 202, 202, 196, 197, 524, 522, 521,   2,   0,   2, 224],
 [ 0, 197, 197, 198, 199, 199, 200, 201, 201, 195, 196, 523, 521, 520,   4,   2,   0, 223],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #fromSink
 ]

TRAVEL_TIMES = [
 [ 0,  45,  45,  45,  44,  44,  44,  43,  43,  46,  46, 676, 675, 674, 224, 224, 223, 0],
 [ 0,   0,   1,   1,   2,   3,   4,   4,   4,   2,   1, 631, 630, 629, 198, 198, 197, 45],
 [ 0,   1,   0,   1,   1,   2,   3,   3,   4,   3,   2, 632, 631, 630, 199, 198, 197, 45],
 [ 0,   1,   1,   0,   1,   1,   2,   3,   3,   3,   2, 632, 631, 630, 200, 199, 198, 45],
 [ 0,   2,   1,   1,   0,   1,   2,   2,   2,   4,   3, 632, 632, 631, 200, 200, 199, 44],
 [ 0,   3,   2,   1,   1,   0,   1,   1,   2,   5,   4, 633, 632, 631, 201, 200, 199, 44],
 [ 0,   4,   3,   2,   2,   1,   0,   1,   1,   6,   5, 633, 632, 632, 202, 201, 200, 44],
 [ 0,   4,   3,   3,   2,   1,   1,   0,   0,   6,   5, 634, 633, 632, 203, 202, 201, 43],
 [ 0,   4,   4,   3,   2,   2,   1,   0,   0,   6,   6, 634, 633, 633, 203, 202, 201, 43],
 [ 0,   2,   3,   3,   4,   5,   6,   6,   6,   0,   1, 630, 629, 628, 196, 196, 195, 46],
 [ 0,   1,   2,   2,   3,   4,   5,   5,   6,   1,   0, 631, 630, 629, 197, 197, 196, 46],
 [ 0, 631, 632, 632, 632, 633, 633, 634, 634, 630, 631,   0,   3,   6, 526, 524, 523, 676],
 [ 0, 630, 631, 631, 632, 632, 632, 633, 633, 629, 630,   3,   0,   3, 524, 522, 521, 675],
 [ 0, 629, 630, 630, 631, 631, 632, 632, 633, 628, 629,   6,   3,   0, 522, 521, 520, 674],
 [ 0, 198, 199, 200, 200, 201, 202, 203, 203, 196, 197, 526, 524, 522,   0,   2,   4, 224],
 [ 0, 198, 198, 199, 200, 200, 201, 202, 202, 196, 197, 524, 522, 521,   2,   0,   2, 224],
 [ 0, 197, 197, 198, 199, 199, 200, 201, 201, 195, 196, 523, 521, 520,   4,   2,   0, 223],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #fromSink
 ]

# Time windows (key: node, value: lower/upper bound)
TIME_WINDOWS_LOWER = {0: 0, 1: 200, 2: 400, 3: 600, 4: 0, 5: 680, 6: 900, 7: 900, 8: 780, 9: 900, 10: 700, 11: 0, 12: 200, 13: 0, 14: 600, 15: 900, 16: 200,}
TIME_WINDOWS_UPPER = {1: 400, 2: 600, 3: 900, 4: 500, 5: 1200, 6: 1000, 7: 1200, 8: 1400, 9: 1000, 10: 1000, 11: 1000, 12: 1500, 13: 800, 14: 900, 15: 1200, 16: 350,}

#TIME_WINDOWS_LOWER = {0: 0, 1: 420, 2: 600, 3: 960, 4: 600, 5: 0, 6: 300, 7: 0, 8: 300, 9: 0, 10: 600, 11: 600, 12: 0, 13: 300, 14: 420, 15: 600, 16: 660}
#TIME_WINDOWS_UPPER = {0: 300, 1: 720, 2: 900, 3: 1080, 4: 780, 5: 300, 6: 600, 7: 240, 8: 600, 9: 180, 10: 960, 11: 900, 12: 300, 13: 600, 14: 480, 15: 900, 16: 900}

# Transform distance matrix into DiGraph
A = array(DISTANCES, dtype=[("cost", int)])
G_d = from_numpy_matrix(A, create_using=DiGraph())

# Transform time matrix into DiGraph
A = array(TRAVEL_TIMES, dtype=[("time", int)])
G_t = from_numpy_matrix(A, create_using=DiGraph())

# Merge
G = nx.compose(G_d,G_t)

# Set time windows
set_node_attributes(G, values=TIME_WINDOWS_LOWER, name="lower")
set_node_attributes(G, values=TIME_WINDOWS_UPPER, name="upper")

# The depot is relabeled as Source and Sink
G = relabel_nodes(G, {0: "Source", 17: "Sink"})

# The VRP is defined and solved
prob = VehicleRoutingProblem(G, num_stops=None, load_capacity=None, duration=None, time_windows=True, pickup_delivery=False, distribution_collection=False, drop_penalty=None, fixed_cost=0, num_vehicles=5, use_all_vehicles=False, periodic=None, mixed_fleet=False, minimize_global_span=False)
#prob = VehicleRoutingProblem(G, time_windows=True)
prob.solve()

print(prob.best_routes_cost)
print(prob.best_routes_duration)
print(prob.best_value)
print(prob.best_routes)
print(prob.arrival_time)
print('the elapsed time:%s'% (round(time.time() - start_time, 4)))
