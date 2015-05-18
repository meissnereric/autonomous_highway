from math import pi

#1600 meters in a mile
class RoadParameters:
    cellLength = 5 #in meters
    initLaneLength = 10 #in cells
    deltaVel = 2.5 #m/s
    maxDeltaVel = 5 #m/s
    baseVel = 25 #m/s
    maxAccel = 2.8 #m/s^2
    maxDecel = -3.0  #m/s^2
    numLanes = 5
    laneVels = [lane * deltaVel + baseVel for lane in range(numLanes)]
    maxCarsPerHourPerLane =  2400 #cars / hour
    maxFlowPerLane = [2400 * (  vel / 32.5) for vel in laneVels]  #cars / hour / lane - Empirical Data - pg 120
    maxFlow = sum(maxFlowPerLane) / 3600
    flowParam = 1
    rAlpha = 1.5
    #flow = maxFlow * flowParam #parameter to alter
    flow = 3 #cars/second?
    #exits = [15,50,100,150, 200]
    mile = 1600 #meters
    exits = [int (float(i * mile) / float(cellLength)) for i in range(1,8)]#in cells
    maxLaneLength = exits[-1] #in cells
    entrances = [int(exit - float(mile)/float(cellLength)) for exit in exits]#in cells
    percentContinuing = 0.9 #percentage of new cars on a road continuing
    maxEpsilonLook = 10  #in cells
    turnTime = 10 #in seconds
    staticUpEpsilon = mile * 0.25 #meters
    staticDownEpsilon = mile * 0.25 #meters
    def getPercentContinuing():
        return percentContinuing

    def getPercentEntering():
        return 1 - percentContinuing

#pg 105
def getTurnTime(vel):
    b = params.maxEpsilonLook * params.cellLength
    a = params.maxAccel
    v_l = vel
    v_d = vel - params.deltaVel
    v_max = v_l + params.maxDeltaVel
    t_a  = (v_max - v_l) / a #time to accelerate to max velocity
    x_a = v_l * t_a + 0.5 * a * (t_a)**2 #car position when max velocity is reached
    x_a_d = b + v_d * t_a
    t_v = (x_a_d - x_a) / (v_max - v_d)

    
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
    return t_a + t_v

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
        self.params = 0
    def newTurn(self, dt):
        self.numMissedCars.append(0)
        self.numMadeCars.append(0)
        self.carsRequestingLC.append(0)
        self.carsInCS.append(0)
        self.carsMakingLC.append(0)
        self.carsDoLC.append(0)
        stats.costPerLaneChange.append(0)
        stats.turnTime.append(0)
    def addAverages(self, stats):
        self.numMissedCars.append(average(stats.numMissedCars))
        self.numMadeCars.append(average(stats.numMadeCars))
        self.carsRequestingLC.append(average(stats.carsRequestingLC))
        self.carsInCS.append(average(stats.carsInCS))
        self.carsMakingLC.append(average(stats.carsMakingLC))
        self.carsDoLC.append(average(stats.carsDoLC))
        self.turnTime.append(average(stats.turnTime))
        self.costPerLaneChange.append(average(stats.costPerLaneChange))
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

    

stats = Statistics()
