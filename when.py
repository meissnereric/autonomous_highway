from math import pi
from params import params, stats

#pg 104
def When(road):
    for car in road.cars:
        car.epsilons = getEpsilons(car.position[1], road)
        car.d_es = sum(epsilons[1:])
        exit = car.exit*params.cellLength
        pos = car.position[0]*params.cellLength
        car.priority =  exit - car.d_es - pos
        if car.d_es < (exit - pos):
            road.C_LC_R.append(car, car.position[1] - 1 )
        elif exit - (car.d_es + car.epsilons[0]) > pos:
            road.C_LC_R.append(car, car.position[1] + 1 )

#pg 105
def getEpsilons(car, road):
    epsilons = []
    times = []
    for lane in range(car.position[1] + 1):
        sideCars = [ocar for ocar in road.cars if (ocar.position[1] == lane+1 or ocar.position[1]==lane-1)
                                                and (ocar.position[0] >= car.position[0] - params.maxEpsilonLook)
                                                and (ocar.position[0] <= car.position[0] + params.maxEpsilonLook)]
        LCD = [LC for LC in sideCars if LC.targetLane != LC.position[1]]
        SD = [nLC for nLC in sideCars if nLC.targetLane == nLC.position[1]]
        OD = [cell for cell in road.lanes[lane].cells if (not (cell.filled))
                                            and (cell.position[0] >= car.position[0] - params.maxEpsilonLook)
                                            and (cell.position[0] <= car.position[0] + params.maxEpsilonLook)]
        R = len(LCD) /( len(OD)+1) + len(SD) - len(LCD)
        T = getTurnTime(lane, road)
        times.append(T)
        epsilons.append(R * T * params.laneVels[lane])
    params.turnTime = max(times)
    return epsilons
#pg 105
def getTurnTime(lane, road):
    b = params.maxEpsilonLook
    a = params.maxAccel
    v_l = params.laneVels[lane]
    v_max = v_l + params.deltaVel
    t_a  = (v_max - v_l) / a #time to accelerate to max velocity
    x_a = v_l * t_a + 0.5 * a * (t_a)**2 #car position when max velocity is reached
    t_max = (pi * b - x_a ) / v_max 
    return t_a + t_max

