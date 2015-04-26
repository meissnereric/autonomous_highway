from params import params, stats

#pg 104
def When(road):
    for car in road.cars:
        car.epsilons = getEpsilons(car, road)
        car.d_es = sum(car.epsilons[:-1])
        exit = car.exit*params.cellLength
        pos = car.position[0]*params.cellLength
        #Priority can really just be.... this. Cool. Approved 4-20-2015 
        car.priority =  (car.d_es) / (exit - pos + 1)
        if exit - car.d_es <= pos and car.position[1]>0:
            car.targetLane = car.position[1] - 1

        elif exit - (car.d_es + car.epsilons[len(car.epsilons)-1]) > pos:
            if car.position[1] < len(road.lanes)-1:
                car.targetLane = car.position[1] + 1

#pg 105
def getEpsilons(car, road):
    epsilons = []
    times = []
    R = params.rAlpha * getR(road)
    T = params.turnTime #todo move this to road.py and call once a turn
    for lane in range(car.position[1] + 1):
        epsilons.append(R * T * params.laneVels[lane])
    return epsilons

def getR( road):
#        sideCars = [ocar for ocar in road.cars if (ocar.position[1] == lane+1 or ocar.position[1]==lane-1)
#                                                and (ocar.position[0] >= car.position[0] - params.maxEpsilonLook)
#                                                and (ocar.position[0] <= car.position[0] + params.maxEpsilonLook)]
#        
#        LCD = [LC for LC in sideCars if LC.targetLane != LC.position[1]]
#        SD = [nLC for nLC in sideCars if nLC.targetLane == nLC.position[1]]
#        OD = [cell for cell in road.lanes[lane].cells if (not (cell.filled))
#                                            and (cell.position[0] >= car.position[0] - params.maxEpsilonLook)
#                                            and (cell.position[0] <= car.position[0] + params.maxEpsilonLook)]
#        
#        R1 = 0
#        R2 = 0
#        R = 0
#        R1 = float(len(LCD)) / float( len(OD)+1) 
#        R2 = float(len(SD))/float( len(LCD)+1)
#        if (not R1 == 0) or (not R2 == 0):
#            R = (R1 + R2)**(-1)
#        
#        if R < 1:
#            R = 1
#
        if stats.carsRequestingLC[road.turn] > stats.carsMakingLC[road.turn] > 0:
            R = float(stats.carsRequestingLC[road.turn]) / float( stats.carsMakingLC[road.turn])
        else:
            R = 1.5
        #TODO actually calculate a good R
        #Try doing the ratio of cars requesting LC vs cars making LC last turn. Will never go below 1. 
#Maybe scale it a litte bit, might be low. 
#Possibly up it dynamically based on #cars missing exit?

        return R
