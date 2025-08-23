import math, numpy as np

class Windmill:

    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name
    #Calculate the fuel consumption of the vessel between two windmills
    def fuelcon(self, windmill):
        #From East to West
        if self.x < windmill.x:
            r = 6373
            
            xDis = abs(math.radians(self.x) - math.radians(windmill.x))
            yDis = abs(math.radians(self.y) - math.radians(windmill.y))

            firstdis = abs(math.sin(xDis / 2)**2 + math.cos(self.x) * math.cos(windmill.x) * math.sin(yDis / 2)**2)
            distance = (2 * math.atan2(np.sqrt(firstdis), np.sqrt(1 - firstdis))) * r

            fuelcon = 1.1 * distance * 30 * 5.5 * (38.89 / (38.89 + 5))/1000
        #From West to East
        else:
            r = 6373

            xDis = abs(math.radians(self.x) - math.radians(windmill.x))
            yDis = abs(math.radians(self.y) - math.radians(windmill.y))

            firstdis = abs(math.sin(xDis / 2)**2 + math.cos(self.x) * math.cos(windmill.x) * math.sin(yDis / 2)**2)
            distance = (2 * math.atan2(np.sqrt(firstdis), np.sqrt(1 - firstdis))) * r

            fuelcon = 1.1 * distance * 30 * 5.5 * (38.89 / (38.89 - 5))/1000

        return fuelcon

    def __repr__(self):
        
        return self.name

class Fitness:

    def __init__(self, route):

        self.route = route
        self.fuelcon = 0
        self.fitness = 0.0

    def routeCons(self):

        if self.fuelcon == 0:
            pathcons = 0
            
            for i in range(0, len(self.route)):
                fromWindmill = self.route[i]
                toWindmill = None

                if i + 1 < len(self.route):
                    toWindmill = self.route[i + 1]

                else:
                    toWindmill = self.route[0]

                pathcons += fromWindmill.fuelcon(toWindmill)
                
            self.fuelcon = pathcons

        return self.fuelcon

    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeCons())
            
        return self.fitness