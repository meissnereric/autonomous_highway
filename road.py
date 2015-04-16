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
        self.FCS = []
        self.clc = []
        self.cars = []
        self.createLanes()
    
    def createLanes(self):        
        #createLanes
        for vel in params.laneVels:
            self.lanes.append(Lane(vel))
        
        for lane in self.lanes:
            lane.cells = []

        #Fill lanes with cells
        #for y, lane in enumerate(self.lanes):
         #   for x in range(params.initLaneLength):
          #      lane.cells.append(Cell(x,y)) 
    
    ###################################################
    ### Define major updates for the Road each turn ###
    ###################################################

    def cleanRoad(self):
        self.clearCarData()
        self.updateExitingCars()
        self.removeOOBCars()
        self.removeExtraCells()

    def updateRoad(self, dt):
        self.addNewCells(dt)
        self.addEnteringCars(dt)
        self.addContinuingCars(dt)
        self.cars.sort(key = lambda c: c.position[0])

    def updateExitingCars(self):
        for car in self.cars:
            if car.position[0] >= car.exit:
                if car.position[1] == 0:
                    self.exitCar(car)
                else:
                    self.markMissedExit(car)

    def exitCar(self, car):
        if len(self.lanes[car.position[1]].cells) > car.position[0]:
            self.lanes[car.position[1]].cells[car.position[0]].filled = False
        self.cars.remove(car)
        stats.numMadeCars[0] += 1
        print 'Car made its exit: ' + str(car.position) + " : " + str(car.exit)
        
    def markMissedExit(self, car):
        if len(self.lanes[car.position[1]].cells) > car.position[0]:
            self.lanes[car.position[1]].cells[car.position[0]].filled = False
        self.cars.remove(car)
        stats.numMissedCars[0] += 1
        print 'Car missed its exit: ' + str(car.position) + " : " + str(car.exit)

    #Tested
    def updateLCs(self):
        for lc in self.clc:
            print "platoon lc"
            for i in range(len(lc[0].cars)):
                print "lc(" + str(lc[0].cars[i].position) + "," + str(lc[1][i].position)
                self.laneChange( (lc[0].cars[i], lc[1][i]) )

    def addNewCells(self, dt):
        self.newCells = [0] * len(self.lanes)
        for y, laneVel in enumerate(params.laneVels):
            dist = dt * laneVel
            numNewCells = int(dist / CL)
            for i in range(numNewCells):
                self.lanes[y].cells.insert(0, Cell(0, y))
                self.newCells[y] += 1
            for car in self.cars:
                if car.position[1] == y:
                    car.position = (car.position[0] + numNewCells, car.position[1])
            for j, cell in enumerate(self.lanes[y].cells):
                    cell.position = (j, cell.position[1])

    def removeOOBCars(self):
        for car in self.cars:
            if car.position[0] > params.maxLaneLength:
                self.markMissedExit(car)
                #todo update stats for deleted cars

    def removeExtraCells(self):
        for lane in self.lanes:
            if(len(lane.cells) >= params.maxLaneLength):
                lane.cells = lane.cells[0 : params.maxLaneLength - 1]

    def addContinuingCars(self, dt):
        numNewCars = int(dt * params.percentContinuing * params.flow)
        for i in range(numNewCars):
            exit = randint(0,len(params.exits)-1)
            lane = self.getLane(exit)
            cell = randint(0, self.newCells[lane]-1)
            while not self.addToCell(Car(cell, lane, params.exits[exit]), self.lanes[lane]):
                cell = randint(0, self.newCells[lane]-1)
                lane = self.getLane(exit,cell)

    
    def addEnteringCars(self, dt):
        numNewCars = int(dt * (1 - params.percentContinuing) * params.flow)
        for i in range(numNewCars):
            entrance = randint(0, len(params.entrances)-1)
            exit = randint(entrance, len(params.exits)-1)
            cell = self.getCellForEntering(entrance, dt)
            i = 0
            while not self.addToCell(Car(cell.position[0], 0, params.exits[exit]), self.lanes[0]) and i < 100:
                cell = self.getCellForEntering(entrance,dt)
                i += 1
    def clearCarData(self):
        for car in self.cars:
            car.accel = 0
        self.FCS = []
        self.clc = []

    ################################################
    ### Define Utility functions for road actions###
    ################################################
    
#returns a random cell in the correct span for that entrance
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
    def getLane(self, exit, cell = 0):
        for y, lane in reversed(list(enumerate(self.lanes))):
            d_es = sum( when.getEpsilons( Car(cell, y, params.exits[exit]), self))
            if params.exits[exit] * CL - d_es > cell*CL:
                return y
        print 'never caught'
        return 0
    
    def addToCell(self, car, lane):
 #       print car.position
#        print len(lane.cells)
        if not (lane.cells[ car.position[0] ].filled):
            lane.cells[car.position[0]].filled = True
            self.cars.append(car)
            return True
        else:
            print "Added a car to a cell that was already filled. (Cell:Lane) = " + str(car.position)
            return False


    def getExit(self, cell, lane):
        ep = when.getEpsilons(Car(cell, lane, -1), self)
        d_es = sum(ep[1:])
        e = [exit for exit in params.exits if exit*CL - d_es > cell*CL]
        if not e:
            return 0
        else:
            return min(e)
    
    #Tested
    #Physically perform a lane change - LC = (car, cell)
    def laneChange(self, LC ):
        car = LC[0]
        cell = LC[1]
        if cell.filled:
            print "Lane changing into a filled cell you fool!" + str(cell.position)
        if len(self.lanes[car.position[1]].cells) > car.position[0]:
            self.lanes[car.position[1]].cells[car.position[0]].filled = False
        car.position = (cell.position)
        if len(self.lanes[cell.position[1]].cells) > cell.position[0]:
            self.lanes[cell.position[1]].cells[cell.position[0]].filled = True

    def addFCS(self, fcs):
        p = Platoon(fcs[0])
        self.FCS.append( (p, fcs[1]) )


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
        self.targetLane=lane
        self.d_es = 0#in meters
        Car.id += 1
        self.id = Car.id
        self.epsilons = []

class Lane:
    def __init__(self, velocity):
        self.cells = []
        self.openings = []
        self.velocity = velocity

    def createOpenings(self, cells):
        self.openings = [cell for cell in cells if not cell.filled]

class Platoon:
    def __init__(self, cars):
        cars.sort(key = lambda c: c.position[0])
        self.cars = cars
        self.position = (cars[0].position[0], cars[0].position[1])
        self.length = len(cars) * params.cellLength
        self.priority = min([car.priority for car in cars])
        self.accel = max([abs(car.accel) for car in cars])

        #if largest accel is backwards
        if self.accel > max ([car.accel for car in cars]):
            self.accel = self.accel * -1
