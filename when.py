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

        #added *2 - 4-29-15 - because have to account for the up AND the down part 
        elif exit - (car.d_es + car.epsilons[-1]*2) > pos:
            if car.position[1] < len(road.lanes)-1:
                car.targetLane = car.position[1] + 1

#pg 105
def getEpsilons(car, road):
    if road.baseCase:
        return getBaseEpsilons(car)
    epsilons = []
    times = []
    R = params.rAlpha * getR(road)
    T = params.turnTime
    for lane in range(car.position[1] + 1):
        epsilons.append(R * T * params.laneVels[lane])
    return epsilons

def getR( road):
        if stats.carsRequestingLC[road.turn] > stats.carsMakingLC[road.turn] > 0:
            R = float(stats.carsRequestingLC[road.turn]) / float( stats.carsMakingLC[road.turn])
        else:
            R = 1.5
        return R


###### Base case static Epsilons ##############
def baseCaseWhen(cars):
    for car in cars:
        car.epsilons = getBaseEpsilons(car)
        d_es = sum(car.epsilons[:-1])
        exit = car.exit*params.cellLength
        pos = car.position[0]*params.cellLength
        if exit - d_es <= pos and car.position[1]>0:
            car.targetLane = car.position[1] - 1

        elif exit - (d_es + car.epsilons[-1]*2) > pos:
            if car.position[1] < params.numLanes-1:
                car.targetLane = car.position[1] + 1
    return cars

def getBaseEpsilons(car):
    numberLC = car.position[1]
    epsilons = []
    for i in range(numberLC):
        epsilons.append(params.staticDownEpsilon)
    epsilons.append(params.staticUpEpsilon)
    return epsilons
