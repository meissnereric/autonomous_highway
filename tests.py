import road
import how
import do
import when
import baseHow
import pickle
import copy
from time import time
from params import *


def noTime(myRoad):
    global stats
    params.turnTime = max([getTurnTime(vel) for vel in params.laneVels])
    stats.params = params
    stats.newTurn(params.turnTime)
    myRoad.updateRoad(params.turnTime)

def tests(myRoad):
    global stats
    myRoad.baseCase = False
    when.When(myRoad)
    stats.carsRequestingLC[myRoad.turn] = len([car for car in myRoad.cars if car.position[1] != car.targetLane])
    how.How(myRoad)
    stats.carsInCS[myRoad.turn] = len(myRoad.FCS)
    
    myRoad.clc = do.do(myRoad.FCS)
    myRoad.computeCost()
    stats.carsDoLC[myRoad.turn] = len(myRoad.clc)
    if myRoad.clc:
        stats.costPerLaneChange[myRoad.turn] = myRoad.totalCost[myRoad.turn] / float(len(myRoad.clc))
    else:
        stats.costPerLaneChange[myRoad.turn] = 0

    myRoad.updateLCs()
    stats.carsMakingLC[myRoad.turn] = myRoad.madeLC
    stats.totalCars[myRoad.turn] = len(myRoad.cars)
    myRoad.cleanRoad()
   # print "Cars requesting LC: " + str(stats.carsRequestingLC[myRoad.turn]) #after when
   # print "Cars in how CS: " + str(stats.carsInCS[myRoad.turn]) #after how
   # print "Cars making do LC: " + str(stats.carsDoLC[myRoad.turn]) #after do
   # print "Cost per lane change: " + str(stats.costPerLaneChange[myRoad.turn])
   # print "Cars really making LC: " + str(stats.carsMakingLC[myRoad.turn]) #after do
   # print "Cars missed exit: " + str(stats.numMissedCars[myRoad.turn])
   # print "Cars made exit: " + str(stats.numMadeCars[myRoad.turn])
   # print "Cars on road: " + str(len(myRoad.cars))

def baseCaseTests(myRoad):
    global stats
    myRoad.baseCase = True
    myRoad.cars = when.baseCaseWhen(myRoad.cars)
    stats.carsRequestingLC[myRoad.turn] = len([car for car in myRoad.cars if car.position[1] != car.targetLane])
    baseHow.baseCaseHow(myRoad)
    stats.carsInCS[myRoad.turn] = len(myRoad.FCS)
    
    myRoad.clc = do.baseCaseDo(myRoad.FCS)
    myRoad.computeCost()
    stats.carsDoLC[myRoad.turn] = len(myRoad.clc)
    if myRoad.clc:
        stats.costPerLaneChange[myRoad.turn] = myRoad.totalCost[myRoad.turn] / float(len(myRoad.clc))
    else:
        stats.costPerLaneChange[myRoad.turn] = 0
    
    myRoad.updateLCs()
    stats.carsMakingLC[myRoad.turn] = myRoad.madeLC
    myRoad.cleanRoad()
   # print "Cars requesting LC: " + str(stats.carsRequestingLC[myRoad.turn]) #after when
   # print "Cars in how CS: " + str(stats.carsInCS[myRoad.turn]) #after how
   # print "Cars making do LC: " + str(stats.carsDoLC[myRoad.turn]) #after do
   # print "Cost per lane change: " + str(stats.costPerLaneChange[myRoad.turn])
   # print "Cars really making LC: " + str(stats.carsMakingLC[myRoad.turn]) #after do
   # print "Cars missed exit: " + str(stats.numMissedCars[myRoad.turn])
   # print "Cars made exit: " + str(stats.numMadeCars[myRoad.turn])
   # print "Cars on road: " + str(len(myRoad.cars))

def viewCar(car):
    print car
    print "Position : Exit : targetLane : epsilons : d_es : priority"
    print str(car.position) + " : " +str(car.exit * params.cellLength) + " : " + str(car.targetLane) + " : " + str(car.d_es)
    print car.priority

def printSameCellCars(myRoad):
    #print 'printing same cell cars'
    for car1 in myRoad.cars:
        for car2 in myRoad.cars:
            if car1 != car2 and car1.position == car2.position:
                viewCar(car1)
                viewCar(car2)
                print car1
                print car2

def viewCars(road):
    for lane in reversed(road.lanes):
        string = ""
        for cell in lane.cells:
            if cell.filled:
                string += "1 "
            else:
                string += "0 "
        print string
        print ''

def lenCarsInLane(l, cars):
    return len([car for car in cars if car.position[1] == l])

def sortCars(cars):
    cars.sort(key = lambda c: c.position[0])

def timer(f, *args):
    s = time()
    f(*args)
    e = time()
    return e - s

def oldTimeSim(f, numIters):
    totalTime = 0
    for i in range(numIters):
        turn2 = timer(noTime, myRoad)
        turn = timer(f, myRoad) + turn2
        stats.turnTime[myRoad.turn] = turn
        totalTime += turn
        print str(turn) + " : " + str(totalTime)
        print ''

#maybe for final results have a "max road length" parameter to change and compare to find how well it scales. 
#6km roads do X fast,  10km roads do X fast
def timeSim(f ,numIters):
    totalTime = 0
    for i in range(numIters):
        noTime(myRoad)
        turn = timer(f, myRoad)
        stats.turnTime[myRoad.turn] = turn
        totalTime += turn
        print str(turn) + " : " + str(totalTime)
        print ''

myRoad = road.Road()


def runBothPc(numIters):
    runPcSims(tests, numIters)
    runPcSims(baseCaseTests, numIters)

def runBothFlow(numIters):
    runFlowSims(tests, numIters)
    runFlowSims(baseCaseTests, numIters)

def runPcSims(f, numIters):
    global myRoad
    simStats = []
    params.flow = 5.5
    simStats.append(params)
    for pc in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        
        stats.reset()
        myRoad = road.Road()
        params.flow = 0.5
        timeSim(f, 100)
        myRoad.turn = -1
        
        print 'pc: ' + str(pc)
        stats.reset()
        myRoad = road.Road()
        print myRoad.turn
        params.percentContinuing = pc
        timeSim(f, numIters)
        simStats.append(copy.copy(stats))
    fileName = str(f.__name__)+ "_uniform_percentCont_01-09_5_20_2015_data.p"
    writeToFile(fileName, simStats)
    return simStats

def runFlowSims(f, numIters):
    global myRoad
    simStats = []
    simStats.append(params)
    for flow in [x * 0.5 for x in range (1,11)]:
        print 'flow: ' + str(flow)
        
        stats.reset()
        myRoad = road.Road()
        params.flow = 0.5
        params.cellLength = 12
        timeSim(f, 100)
        myRoad.turn = -1
        
        stats.reset()
        params.flow = flow
        timeSim(f, numIters)
        simStats.append(copy.copy(stats))
    fileName = str(f.__name__)+ "_cellLength12_flow_0.5-5_7_6_2015_data.p"
    writeToFile(fileName, simStats)
    return simStats

def readAndAverage(fileName):
    tempStats = readFromFile(fileName)
    tempParams = tempStats[0]
    tempStats = tempStats[1:]
    averages = Statistics()
    mins = Statistics()
    maxs = Statistics()
    for run in tempStats:
        averages.addAverages(run)
        mins.addMin(run)
        maxs.addMax(run)
    return (tempParams, tempStats, averages, mins, maxs)

def writeToFile( fileName, stats):
    with open(fileName, "wb") as f:
        pickle.dump(stats, f)
    with open(fileName, "rb") as f:
        print pickle.load(f)
def readFromFile( fileName):
    with open(fileName, "rb") as f:
        return pickle.load(f)
