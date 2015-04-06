import road
import how
import do
import when
from params import params

myRoad = road.Road()
myRoad.initCars()

def tests(myRoad):
    myRoad.updateRoad(5, [])
    #myRoad.updateRoad(4, [(myRoad.cars[0], road.Cell(2,1))])
    return myRoad

def viewCars(road):
    for lane in reversed(road.lanes):
        string = ""
        for cell in lane.cells:
            if cell.filled:
                string += "1 "
            else:
                string += "0 "
        print string

myRoad = tests(myRoad)
