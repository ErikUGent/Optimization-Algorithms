import math, numpy as np

class Windmill:

    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name

    def distance(self, windmill):

        r = 6373
        xDis = abs(math.radians(self.x) - math.radians(windmill.x))
        yDis = abs(math.radians(self.y) - math.radians(windmill.y))

        firstdis = abs(math.sin(xDis / 2)**2 + math.cos(self.x) * math.cos(windmill.x) * math.sin(yDis / 2)**2)
        distance = (2 * math.atan2(np.sqrt(firstdis), np.sqrt(1 - firstdis))) * r
        print(distance)
        return distance

    def __repr__(self):
        
        return self.name

class Fitness:

    def __init__(self, route):

        self.route = route
        self.distance = 0
        self.fitness= 0.0

    def routeDistance(self):

        if self.distance ==0:
            pathDistance = 0
            
            for i in range(0, len(self.route)):
                fromWindmill = self.route[i]
                toWindmill = None

                if i + 1 < len(self.route):
                    toWindmill = self.route[i + 1]

                else:
                    toWindmill = self.route[0]
                    #toWindmill = self.route[i]

                pathDistance += fromWindmill.distance(toWindmill)
                
            self.distance = pathDistance

        return self.distance

    

    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
            
        return self.fitness