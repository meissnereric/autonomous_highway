import road
import how
import do
import when
from time import time
from params import *


params.turnTime = max([getTurnTime(vel) for vel in params.laneVels])
def tests(myRoad):
    stats.newTurn(params.turnTime)
    myRoad.updateRoad(params.turnTime)
    #viewCars(myRoad)
    when.When(myRoad)
    how.How(myRoad)
    myRoad.clc = do.do(myRoad.FCS)
    myRoad.updateLCs()
    myRoad.cleanRoad()
    print "Cars missed exit: " + str(stats.numMissedCars[0])
    print "Cars made exit: " + str(stats.numMadeCars[0])
    print "Cars on road: " + str(len(myRoad.cars))

def viewCar(car):
    print car
    print "Position : Exit : targetLane : epsilons : d_es"
    print str(car.position) + " : " +str(car.exit) + " : " + str(car.targetLane) + " : " + str(car.d_es)

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

numIters = 100

#maybe for final results have a "max road length" parameter to change and compare to find how well it scales. 
#6km roads do X fast,  10km roads do X fast
def timeSimulation():
    totalTime = 0
    for i in range(numIters):
        turn = timer(tests, myRoad)
        totalTime += turn
        print str(turn) + " : " + str(totalTime)

myRoad = road.Road()
tests(myRoad)
#viewCars(myRoad)


