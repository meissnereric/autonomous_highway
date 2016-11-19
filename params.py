from math import pi

#1600 meters in a mile
class RoadParameters:
    def __init__(self):
        self.cellLength = 5 #in meters
        self.initLaneLength = 10 #in cells
        self.deltaVel = 2 #m/s
        self.maxDeltaVel = 5 #m/s
        self.baseVel = 26 #m/s
        self.maxAccel = 2.8 #m/s^2
        self.maxDecel = -3.0  #m/s^2
        self.numLanes = 5
        self.laneVels = [lane * self.deltaVel + self.baseVel for lane in range(self.numLanes)]
        self.rAlpha = 1.5
        self.flow = 0.5 #cars/second?
        self.mile = 1600 #meters
        self.numExits = 20
        self.exits = [int (float(i * 500) / float(self.cellLength)) for i in range(5,self.numExits)]#in cells
        self.exitingRate = [ 1.0 / len(self.exits) for i in self.exits] #of cars that do exit, how are they distributed
        self.overallExitRate = 1.0 #how many cars end up continuing along the road in the end, never exit
        self.maxLaneLength = self.exits[-1] #in cells
        self.entrances = [int(exit - float(500)/float(self.cellLength)) for exit in self.exits]#in cells
        self.percentContinuing = 0.2 #percentage of new cars on a road continuing
        self.maxEpsilonLook = 15  #in cells
        self.staticUpEpsilon = self.mile * 0.25 #meters
        self.staticDownEpsilon = self.mile * 0.25 #meters
        self.turnTime = self.getTurnTime(max(self.laneVels))

    def getPercentContinuing():
        return percentContinuing

    def getPercentEntering():
        return 1 - percentContinuing

#pg 105
    def getTurnTime(self, vel):
        b = self.maxEpsilonLook * self.cellLength
        a = self.maxAccel
        v_l = vel
        v_d = vel - self.deltaVel
        v_max = v_l + self.maxDeltaVel
        t_a  = (v_max - v_l) / a #time to accelerate to max velocity
        x_a = v_l * t_a + 0.5 * a * (t_a)**2 #car position when max velocity is reached
        x_a_d = b + v_d * t_a
        t_v = (x_a_d - x_a) / (v_max - v_d)
        return t_a + t_v

    
   # print ''
   # print "b : a : v_l : v_max : t_a : x_a : t_max : t_a+t_max"
   # print b
   # print a
   # print v_l
   # print v_max
   # print t_a
   # print x_a
   # print t_v
   # print t_a + t_v

params = RoadParameters()

class Statistics:
    
    def __init__(self):
        self.numMissedCars = []
        self.numMadeCars = []
        self.carsRequestingLC = []
        self.carsInCS = []
        self.carsMakingLC = []
        self.carsDoLC = []
        self.costPerLaneChange = []
        self.turnTime = []
        self.statsPerSim = []
        self.totalCars = []
        self.params = 0
        self.g = []
    def newTurn(self, dt):
        self.numMissedCars.append(0)
        self.numMadeCars.append(0)
        self.carsRequestingLC.append(0)
        self.carsInCS.append(0)
        self.carsMakingLC.append(0)
        self.carsDoLC.append(0)
        stats.costPerLaneChange.append(0)
        stats.turnTime.append(0)
        stats.totalCars.append(0)
    def addMax(self, stats):
        self.numMissedCars.append(halfMax(stats.numMissedCars))
        self.numMadeCars.append(halfMax(stats.numMadeCars))
        self.carsRequestingLC.append(halfMax(stats.carsRequestingLC))
        self.carsInCS.append(halfMax(stats.carsInCS))
        self.carsMakingLC.append(halfMax(stats.carsMakingLC))
        self.carsDoLC.append(halfMax(stats.carsDoLC))
        self.turnTime.append(halfMax(stats.turnTime))
        self.costPerLaneChange.append(halfMax(stats.costPerLaneChange))
        if self.totalCars:
            self.totalCars.append(halfMax(stats.totalCars))
        self.g.append(self.numMissedCars[-1] / self.numMadeCars[-1])
    def addMin(self, stats):
        self.numMissedCars.append(halfMin(stats.numMissedCars))
        self.numMadeCars.append(halfMin(stats.numMadeCars))
        self.carsRequestingLC.append(halfMin(stats.carsRequestingLC))
        self.carsInCS.append(halfMin(stats.carsInCS))
        self.carsMakingLC.append(halfMin(stats.carsMakingLC))
        self.carsDoLC.append(halfMin(stats.carsDoLC))
        self.turnTime.append(halfMin(stats.turnTime))
        self.costPerLaneChange.append(halfMin(stats.costPerLaneChange))
        if self.totalCars:
            self.totalCars.append(halfMin(stats.totalCars))
        self.g.append(self.numMissedCars[-1] / self.numMadeCars[-1])
    def addAverages(self, stats):
        self.numMissedCars.append(average(stats.numMissedCars))
        self.numMadeCars.append(average(stats.numMadeCars))
        self.carsRequestingLC.append(average(stats.carsRequestingLC))
        self.carsInCS.append(average(stats.carsInCS))
        self.carsMakingLC.append(average(stats.carsMakingLC))
        self.carsDoLC.append(average(stats.carsDoLC))
        self.turnTime.append(average(stats.turnTime))
        self.costPerLaneChange.append(average(stats.costPerLaneChange))
        if self.totalCars:
            self.totalCars.append(average(stats.totalCars))
        self.g.append(self.numMissedCars[-1] / self.numMadeCars[-1])
    def reset(self):
        self.numMissedCars = []
        self.numMadeCars = []
        self.carsRequestingLC = []
        self.carsInCS = []
        self.carsMakingLC = []
        self.carsDoLC = []
        self.costPerLaneChange = []
        self.turnTime = []
        self.statsPerSim = []
        self.params = 0

def printStats(stats):
    print 'numMissedCars'
    print stats.numMissedCars
    print ''
    print 'numMadeCars'
    print stats.numMadeCars
    print ''
    print 'cost per lane change'
    print stats.costPerLaneChange
    print ''
    print 'turnTime'
    print stats.turnTime
    print ''

def average(bigLst):
    if bigLst:
        goodData = len(bigLst) / 2
        lst = bigLst[-1 * goodData:] #only take the last half of the data. Because the road has to warm up always
        return float(sum(lst))/ float(len(lst))
    else:
        return 0.0

def halfMax(bigLst):
    if bigLst:
        goodData = len(bigLst) / 2
        lst = bigLst[-1 * goodData:] #only take the last half of the data. Because the road has to warm up always
        return float(max(lst))
    else:
        return 0.0
def halfMin(bigLst):
    if bigLst:
        goodData = len(bigLst) / 2
        lst = bigLst[-1 * goodData:] #only take the last half of the data. Because the road has to warm up always
        return float(min(lst))
    else:
        return 0.0
stats = Statistics()
