# ACO based V-Shape algorithm for distance and formation optimization of a flock of drones with precalculated distance matrix
# Influence of the angle of attack and the speed of the wind are taken into account

from threading import Thread
import numpy as np
import math as math

rho = 1.225 # density of the surrounding air
v_f = 10 # speed of the flock
v_w = 5 # wind speed
alpha = math.radians(90) # angle of attack
v_sq = (v_f + v_w)**2
v_w_sq = (v_w)**2
num_birds = 16 # number of birds in the flock 

num_birds_ref = num_birds/2
ER_ref = 0.9 # reference energy recovery coefficient
A_bird = 0.5 # surface of a drone
v = (v_sq*v_f)-v_w_sq
A_vert = A_bird # surface opposite to drag of a vertical configuration
A_horz = A_bird*num_birds # surface opposite to drag of a horizontal configuration
A_squa = A_bird*np.sqrt(num_birds) # surface opposite to drag of a square configuration
A_diam = A_bird*np.sqrt(num_birds) # surface opposite to drag of a diamond configuration
A_vsha = (1.5*A_bird + (num_birds-3)*(A_bird/8)) # surface opposite to drag of a v-shape configuration
sur_ref = A_vsha # reference surface opposite to drag
CW_ref = 0.50 # reference drag coefficient

class VSHAPE:
    class Flock(Thread):
        def __init__(self,
                     init_location,
                     possible_locations,
                     energy_map,
                     distance_callback,
                     gamma,
                     delta,
                     energy_recovery_coefficient,
                     energy_constant,
                     iterations,
                     cw,
                     sur,
                     first_pass=False):
            Thread.__init__(self)

            self.init_location = init_location
            self.possible_locations = possible_locations
            self.route = []
            self.distance_traveled = 0.0
            self.work_performed = 0.0
            self.location = init_location
            self.energy_map = energy_map
            self.distance_callback = distance_callback
            self.gamma = gamma
            self.delta = delta
            self.energy_recovery_coefficient = energy_recovery_coefficient
            self.energy_constant = energy_constant
            self.iteration = iterations
            self.cw = cw
            self.sur = sur
            self.first_pass = first_pass
            self.update_route(init_location)

            self.tour_complete = False

        def run(self):
            while self.possible_locations:
                nxt = self.pick_path()
                self.traverse(self.location, nxt)
            self.possible_locations.append(self.init_location)
            self.traverse(self.location, self.init_location)
            self.tour_complete = True

        def pick_path(self):
            if self.first_pass:
                import random
                rnd = random.choice(self.possible_locations)
                while rnd == self.init_location and len(self.possible_locations) > 1:
                    rnd = random.choice(self.possible_locations)
                return rnd

            attractiveness = dict()
            sum_total = 0.0  
            for possible_next_location in self.possible_locations:
                    energy_amount = float(self.energy_map[self.location][possible_next_location])
                    distance = float(self.distance_callback(self.location, possible_next_location))
                    dist_1 = float((self.sur*self.cw)/(sur_ref*CW_ref))
                    dist_2 = (dist_1*distance)
 
                    attractiveness[possible_next_location] = pow(energy_amount, self.gamma) * pow(1 / dist_2,
                                                                                                 self.delta) 
                    sum_total += attractiveness[possible_next_location]

            if sum_total == 0.0:
                def next_up(x):
                    import math
                    import struct
                    if math.isnan(x) or (math.isinf(x) and x > 0):
                        return x
                    if x == 0.0:
                        x = 0.0
                    n = struct.unpack('<q', struct.pack('<d', x))[0]
                    if n >= 0:
                        n += 1
                    else:
                        n -= 1
                    return struct.unpack('<d', struct.pack('<q', n))[0]

                for key in attractiveness:
                    attractiveness[key] = next_up(attractiveness[key])
                sum_total = next_up(sum_total)
            import random
            toss = random.random()

            cummulative = 0
            for possible_next_location in attractiveness:
                weight = (attractiveness[possible_next_location] / sum_total)
                if toss <= weight + cummulative:
                    return possible_next_location
                cummulative += weight

        def traverse(self, start, end):
            self.update_route(end)
            self.update_distance_traveled(start, end)
            self.location = end

        def update_route(self, new):
            self.route.append(new)
            self.possible_locations = list(self.possible_locations)
            self.possible_locations.remove(new)

        def update_distance_traveled(self, start, end):
        #   Distance traveled in function of the reference distance    
            dist_trav = float(self.distance_callback(start, end))
            dist_trav_1 = float((self.sur*self.cw)/(sur_ref*CW_ref))        
            dist_trav_2 = (dist_trav_1*dist_trav)
        #   Energy needed to overcome drag.
            work_perf = ((((0.5*rho*v_sq*v_f*self.cw*self.sur)/self.energy_recovery_coefficient) - (0.5*rho*v_sq*((math.sin(alpha/2))**3)*v_w*self.cw*self.sur)))*dist_trav
            self.distance_traveled += dist_trav_2
            self.work_performed += work_perf

        def get_route(self):
            if self.tour_complete:
                return self.route
            return None

        def get_distance_traveled(self):
            if self.tour_complete:
                return round(self.distance_traveled, 0)
            return None
        
        def get_work_performed(self):
            if self.tour_complete:
                return round(self.work_performed, 0)
            return None

    def __init__(self,
                 nodes_num,
                 distance_matrix,
                 start,
                 Flock_count,
                 gamma,
                 delta,
                 energy_recovery_coefficient,
                 energy_constant,
                 iterations,
                 cw,
                 sur):
        self.nodes = list(range(nodes_num))
        self.nodes_num = nodes_num
        self.distance_matrix = distance_matrix
        self.energy_map = self.init_matrix(nodes_num)
        self.Flock_updated_energy_map = self.init_matrix(nodes_num)
        self.start = 0 if start is None else start
        self.Flock_count = Flock_count
        self.gamma = float(gamma)
        self.delta = float(delta)
        self.energy_recovery_coefficient = float(energy_recovery_coefficient)
        self.energy_constant = float(energy_constant)
        self.iterations = iterations
        self.cw = cw
        self.sur = sur
        self.first_pass = True
        self.Flocks = self._init_Flocks(self.start)
        self.shortest_distance = None
        self.shortest_path_seen = None
        self.minimal_work = None

    def get_distance(self, start, end):
        return self.distance_matrix[start][end]

    def init_matrix(self, size, value=0.0):
        ret = []
        for row in range(size):
            ret.append([float(value) for _ in range(size)])
        return ret

    def _init_Flocks(self, start):
        if self.first_pass:
            return [self.Flock(start, self.nodes, self.energy_map, self.get_distance,
                             self.gamma, self.delta, self.energy_recovery_coefficient, self.energy_constant, self.iterations, self.cw, self.sur, first_pass=True) for _ in range(self.Flock_count)]
        for Flock in self.Flocks:
            Flock.__init__(start, self.nodes, self.energy_map, self.get_distance, self.gamma, self.delta, self.energy_recovery_coefficient, self.energy_constant, self.iterations, self.cw, self.sur)

    def update_energy_map(self):
        for start in range(len(self.energy_map)):
            for end in range(len(self.energy_map)):
                self.energy_map[start][end] *= (1 - self.energy_recovery_coefficient)
                self.energy_map[start][end] += self.Flock_updated_energy_map[start][end]

    def populate_Flock_updated_energy_map(self, Flock):
        route = Flock.get_route()
        for i in range(len(route) - 1):
            current_energy_value = float(self.Flock_updated_energy_map[route[i]][route[i + 1]])
            new_energy_value = self.energy_constant / Flock.get_distance_traveled()

            self.Flock_updated_energy_map[route[i]][route[i + 1]] = current_energy_value + new_energy_value
            self.Flock_updated_energy_map[route[i + 1]][route[i]] = current_energy_value + new_energy_value

    def mainloop(self):
        for it in range(self.iterations):
            for Flock in self.Flocks:
                Flock.start()
            for Flock in self.Flocks:
                Flock.join()

            for Flock in self.Flocks:
                self.populate_Flock_updated_energy_map(Flock)
                if not self.shortest_distance:
                    self.shortest_distance = Flock.get_distance_traveled()
                    self.minimal_work = Flock.get_work_performed()

                if not self.shortest_path_seen:
                    self.shortest_path_seen = Flock.get_route()

                if Flock.get_distance_traveled() < self.shortest_distance:
                    self.shortest_distance = Flock.get_distance_traveled()
                    self.shortest_path_seen = Flock.get_route()
                    self.minimal_work = Flock.get_work_performed()

            self.update_energy_map()

            if self.first_pass:
                self.first_pass = False

            self._init_Flocks(self.start)

            self.Flock_updated_energy_map = self.init_matrix(self.nodes_num, value=0)
            if (it + 1) % 50 == 0:
                print('{0}/{1} Searching...'.format(it + 1, self.iterations))

        ret = []
        for ids in self.shortest_path_seen:
            ret.append(self.nodes[ids])

        return ret

START = None
FLOCK_COUNT = 30 # Number of flocks used in the algorithm
GAMMA = 1.1
DELTA = 1.1
ENER_CONSTANT = 3000.0
ITERATIONS = 300 # Number of iterations
# Energey recovery coefficient for flocks flying in vertical, V-Shape, diamond, square, horizontal configuration
ENER_REC_COEFF = [0.8, 0.9, 0.6, 0.6, 0.2]
# Drag coefficient for flocks flying in vertical, V-Shape, diamond, square, horizontal configuration
CW = [1.17, 0.5, 0.8, 1.05, 1.17]
# Surface opposite to drage for flocks flying in vertical, V-Shape, diamond, square, horizontal configuration
SUR = [A_vert, A_vsha, A_diam, A_squa, A_horz]

def main():
    distance_matrix = np.loadtxt(open('distance_matrix.txt', 'rb'), delimiter=' ')
    for index in range(0, len(CW)):
        CWX = CW[index]
        SURX = SUR[index]
        ENER_REC_COEFFX = ENER_REC_COEFF[index]
        colony = VSHAPE(len(distance_matrix[0]),
                 distance_matrix,
                 START,
                 FLOCK_COUNT,
                 GAMMA,
                 DELTA,
                 ENER_REC_COEFFX,
                 ENER_CONSTANT,
                 ITERATIONS,
                 CWX,
                 SURX)
        answer = colony.mainloop()
        print(CWX)
        print(ENER_REC_COEFFX)
        print(np.array(answer) + 1)
        print(colony.shortest_distance)
        print(colony.minimal_work)

if __name__ == '__main__':
    main()