from math import floor
from random import randint
from params import params, stats
import when
CL = params.cellLength
class Road:
    
    ###################################################
    ### Define Road Initialization Functions        ###
    ###################################################
    def __init__(self):
        self.lanes = []
        self.createLanes()
    
    def createLanes(self):        
        #createLanes
        for vel in params.laneVels:
            self.lanes.append(Lane(vel))
        
        for lane in self.lanes:
            lane.cells = []

        #Fill lanes with cells
        for y, lane in enumerate(self.lanes):
            for x in range(params.initLaneLength):
                lane.cells.append(Cell(x,y)) 
    
    def initCars(self):
        self.cars = []
        finalCellPosition = self.lanes[0].cells[len(self.lanes[0].cells) - 1].position[0]
        for y, lv in enumerate(params.laneVels):
            time = float(finalCellPosition*CL) / lv
            numCars = int(time * params.flow)
            for i in range(numCars):
                cell = randint(0, len(self.lanes[y].cells) - 1)
                j=0
                while(self.lanes[y].cells[cell].filled and j < 100):
                    cell = randint(0, len(self.lanes[y].cells) - 1)
                    j=j + 1
                exit = self.getExit(cell, y)
                self.addToCell( Car(cell, y, exit), self.lanes[y])

    ###################################################
    ### Define major updates for the Road each turn ###
    ###################################################

    def updateRoad(self, dt, LC):
        self.clearCarData()
        self.updateLCs(LC)
        self.updateExitingCars(dt)
        self.addNewCells(dt)
        self.addEnteringCars(dt)
        self.addContinuingCars(dt)

    def updateExitingCars(self, dt):
        for car in self.cars:
            if car.position[0] >= car.exit:
                if car.position[1] == 0:
                    self.exitCar(car)
                else:
                    self.markMissedExit(car)

    def exitCar(self, car):
        print str(car.position) + "un-filled"
        self.lanes[car.position[1]].cells[car.position[0]].filled = False
        self.cars.remove(car)

        print 'Car made its exit: ' + str(car.exit)

    def markMissedExit(self, car):
        print str(car.position) + "un-filled"
        self.lanes[car.position[1]].cells[car.position[0]].filled = False
        self.cars.remove(car)
        print 'Car missed its exit: ' + str(car.exit)
        
    #Tested
    def updateLCs(self, LC):
        for lc in LC:
            self.laneChange(lc)
    
    def addNewCells(self, dt):
        self.newCells = [0] * len(self.lanes)
        for y, laneVel in enumerate(params.laneVels):
            dist = dt * laneVel
            numNewCells = int(dist / CL)
            print "numNewCells[" + str(y) + "] = " + str(numNewCells)
            for i in range(numNewCells):
                self.lanes[y].cells.insert(0, Cell(0, y))
                self.newCells[y] += 1
            for car in self.cars:
                if car.position[1] == y:
                    car.position = (car.position[0] + numNewCells, car.position[1])

    def removeExtraCells(self):
        for lane in self.lanes:
            if(len(lane.cells) >= params.maxLaneLength):
                lane.cells = lane.cells[(len(lane.cells) - params.maxLaneLength) : len(lane.cells) -1]

    def addContinuingCars(self, dt):
        
        numNewCars = int(dt * params.percentContinuing * params.flow)
        print "continuing new cars: " + str(numNewCars)
        for i in range(numNewCars):
            exit = randint(0,len(params.exits)-1)
            lane = self.getLane(exit)
            cell = randint(0, self.newCells[lane]-1)
            self.addToCell(Car(cell, lane, params.exits[exit]), self.lanes[lane])
    
    def addEnteringCars(self, dt):
        numNewCars = int(dt * (1 - params.percentContinuing) * params.flow)
        print "entering new cars: " + str(numNewCars)
        for i in range(numNewCars):
            entrance = randint(0, len(params.entrances)-1)
            exit = randint(entrance, len(params.exits)-1)
            cell = self.getCellForEntering(entrance, dt)
            self.addToCell(Car(cell.position[0], 0, params.exits[exit]), self.lanes[0])
    
    def clearCarData(self):
        for car in self.cars:
            car.accel = 0
        params.turnTime = -1

    ################################################
    ### Define Utility functions for road actions###
    ################################################
    
    def getCellForEntering(self, entrance, dt):
        distance = dt * params.laneVels[0]
        startCell = max([cell for cell in self.lanes[0].cells if cell.position[0] <= entrance], key= lambda c: c.position[0])
        if(entrance - distance > 0):
            endCell = max([cell for cell in self.lanes[0].cells if cell.position[0] <= entrance - distance], key= lambda c: c.position[0])
        else:
            endCell = self.lanes[0].cells[len(self.lanes[0].cells)-1]
        targetCell = randint(startCell.position[0], endCell.position[0])
        i=0
        while self.lanes[0].cells[targetCell].filled and i < distance:
            targetCell = randint(startCell.position[0], endCell.position[0])
            i+=1
        return self.lanes[0].cells[targetCell]

    #Used in addContinuous to find the lane for a car with a random exit
    def getLane(self, exit, cell = -1):
        if cell == -1:
            cell = len(self.lanes[0].cells)
        for y, lane in enumerate(self.lanes):
            d_es = sum( when.getEpsilons( Car(cell, y, params.exits[exit]), self))
            if params.exits[exit] * CL - d_es > cell*CL:
                return y
        return len(self.lanes) - 1
    
    def addToCell(self, car, lane):
        if not (lane.cells[ car.position[0] ].filled):
            lane.cells[car.position[0]].filled = True
            self.cars.append(car)
        else:
            print "Added a car to a cell that was already filled. \n (Cell:Lane) = " + str(car.position)


    def getExit(self, cell, lane):
        ep = when.getEpsilons(Car(cell, lane, -1), self)
        d_es = sum(ep[1:])
        return min([exit for exit in params.exits if exit*CL - d_es > cell*CL])
    
    #Tested
    #Physically perform a lane change - LC = (car, cell)
    def laneChange(self, LC ):
        car = LC[0]
        cell = LC[1]
        cell.filled = True
        car.position = (cell.position)
        self.lanes[cell.position[1]].cells[cell.position[0]].filled = False
    
############### End Road class ##############

class Cell:
    id = -1
    def __init__(self, index, lane):
        self.filled = False
        self.position = (index, lane)
        Cell.id += 1
        self.id = Cell.id
class Car:
    id = -1
    def __init__(self, cell, lane, exit):
        if cell == -1:
            cell = len(self.lanes.cells)
        self.position = (cell,lane) #not in meters, in positions
        self.exit=exit #cell position
        self.priority=0
        self.targetLane=0
        self.d_es = 0#in meters
        Car.id += 1
        self.id = Car.id

class Lane:
    def __init__(self, velocity):
        self.cells = []
        self.openings = []
        self.velocity = velocity

    def createOpenings(self, cells):
        self.openings = [cell for cell in cells if not cell.filled]

