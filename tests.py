import road
import how
import do
import when
from time import time
from params import *


params.turnTime = max([getTurnTime(vel) for vel in params.laneVels])
def tests(myRoad):
    stats.newTurn(params.turnTime)
    j=0
    print j
    j += 1
    myRoad.updateRoad(params.turnTime)
    print j
    j += 1
    printSameCellCars(myRoad)
    print j
    j += 1
    #viewCars(myRoad)
    when.When(myRoad)
    print j
    j += 1
    stats.carsRequestingLC[myRoad.turn] = len([car for car in myRoad.cars if car.position[1] != car.targetLane])
    how.How(myRoad)
    stats.carsInCS[myRoad.turn] = len(myRoad.FCS)
    myRoad.clc = do.do(myRoad.FCS)
    stats.carsMakingLC[myRoad.turn] = len(myRoad.clc)
    myRoad.updateLCs()
    myRoad.cleanRoad()
    print "Cars requesting LC: " + str(stats.carsRequestingLC[myRoad.turn]) #after when
    print "Cars in CS: " + str(stats.carsInCS[myRoad.turn]) #after how
    print "Cars making LC: " + str(stats.carsMakingLC[myRoad.turn]) #after do
    print "Cars missed exit: " + str(stats.numMissedCars[myRoad.turn])
    print "Cars made exit: " + str(stats.numMadeCars[myRoad.turn])
    print "Cars on road: " + str(len(myRoad.cars))

def viewCar(car):
    print car
    print "Position : Exit : targetLane : epsilons : d_es : priority"
    print str(car.position) + " : " +str(car.exit * params.cellLength) + " : " + str(car.targetLane) + " : " + str(car.d_es)
    print car.priority

def printSameCellCars(myRoad):
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

#maybe for final results have a "max road length" parameter to change and compare to find how well it scales. 
#6km roads do X fast,  10km roads do X fast
def timeSim(numIters):
    totalTime = 0
    for i in range(numIters):
        turn = timer(tests, myRoad)
        totalTime += turn
        print str(turn) + " : " + str(totalTime)

myRoad = road.Road()


