from params import params
class How:
    def __init__(self, road):
        this.road = road

    def ComputeHow():
        for lane in makeActiveLanes:
            tempCars = [car for car in road.cars if car.position[1] == lane + 1
                                                or car.position[1] == lane - 1]
        OS = getOpeningSets()
        for os in OS:
            (carsUp, carsDown) = getCars(tempCars, os)
            CS = makeCarSets(carsUp)
            CS.extend(makeCarSets(carsDown))
            finalCS = getBestCS(CS, os)
            road.addFCS(finalCS)#todo add as platoon set for do
            removeCars(tempCars, CS)

    def getOpeningSets():
        OS = []
        for lane in this.ActiveLanes:
            OS.extend([cell for cell in road.lanes[lane] if not cell.filled])

    def removeCars(tempCars, CS):
        for car in CS:
            tempCars.remove(car)

    def makeActiveLanes(road):
        ActiveLanes = []
        for car in road.cars:
            if(car.targetLane != car.position[1]):
                if not (car.targetLane in ActiveLanes):
                    ActiveLanes.append(car.targetLane)
        return ActiveLanes

    def makeCarSets(cars, OS):
        CS = []
        for i in range(len(cars) - len(OS)):
            CS.append(cars[0+i, len(OS) + i])
        return CS

##########################GetCars utilities  ########################################
    #pg 107-108
    def getCars(tempCars, os):
        blockUp = [car for car in tempCars if car.position[1] == os[0].position[1] + 1
                                            and car.position[0] <= os[len(os)-1].position[0]
                                            and car.position[0] >= os[0].position[0] ]

        blockDown = [car for car in tempCars if car.position[1] == os[0].position[1] - 1
                                            and car.position[0] <= os[len(os)-1].position[0]
                                            and car.position[0] >= os[0].position[0] ]
        z_u = len(os) - len(blockUp)
        z_d = len(os) - len(blockDown)
        Z = (z_u, z_d)
        
        (ebRU, ebLU, ebRD, ebLD) = EBP = getEdgeBlockingPositions(tempCars)
        possibleCars = getCarsInBounds(tempCars, EBP)
        (CRU, CLU, CRD, CLD) = finalCars = trimLengths(possibleCars, Z)
        CU = CRU.extend(CLU).extend(blockUp)
        CD = CRD.extend(CLD).extend(blockDown)
        return (CU, CD)


    def trimLengths((CRU, CLU, CRD, CLD), (z_u, z_d)):
        if(len(CRU) > z_u):
            CRU = CRU[0:z_u]
        if(len(CLU) > z_u):
            CLU = CLU[len(CLU) - z_u : len(CLU)]
        if(len(CRD) > z_d):
            CRD = CRD[0:z_d]
        if(len(CLD) > z_d):
            CLD = CLD[len(CLD) - z_d : len(CLD)]

        
    #pg 108
    def getEdgeBlockingPositions(tempCars, os):

        ##############Right Up ####################
        ebRUC = [car for car in tempCars if car.position[1] == os[0].position[1] + 1
                                        and car.position[0] <= os[len(os)-1].position[0] + params.maxEpsilonLook
                                        and car.position[0] > os[len(os)-1].position[0] ]
        if(not ebRUC):
            ebRU = os[len(os)-1] + params.maxEpsilonLook
        else:
            ebRU = min([car.position[0] for car in ebRUC])

        ##############Left Up #################
        ebLUC = [car for car in tempCars if car.position[1] == os[0].position[1] + 1
                                        and car.position[0] >= os[0].position[0] - params.maxEpsilonLook
                                        and car.position[0] < os[0].position[0] ]
        if(not ebLUC):
            ebLU = os[len(os)-1] - params.maxEpsilonLook
        else:
            ebLU = max([car.position[0] for car in ebLUC])

        ##############Right Down#############
        ebRDC = [car for car in tempCars if car.position[1] == os[0].position[1] - 1
                                        and car.position[0] <= os[len(os)-1].position[0] + params.maxEpsilonLook
                                        and car.position[0] > os[len(os)-1].position[0] ]
        if(not ebRDC):
            ebRD = os[len(os)-1] + params.maxEpsilonLook
        else:
            ebRD = min([car.position[0] for car in ebRDC])

        #############Left Down################
        ebLDC = [car for car in tempCars if car.position[1] == os[0].position[1] - 1
                                        and car.position[0] >= os[0].position[0] - params.maxEpsilonLook
                                        and car.position[0] < os[0].position[0] ]
        if(not ebLDC):
            ebLD = os[len(os)-1] - params.maxEpsilonLook
        else:
            ebLD = max([car.position[0] for car in ebLDC])
        
        #return the positions
        return (ebRU, ebLU, ebRD, ebLD)
        
    #pg 108 (sort of) - see Drive documentation if wrong
    def getCarsInBounds(tempCars, (ebRU, ebLU, ebRD, ebLD) , os):
        CRU = [car for car in tempCars if car.position[1] == os[0].position[1] + 1
                                       and car.position[0] <= ebRU
                                       and car.position[0] > os[len(os)-1].position[0] ]
        CLU = [car for car in tempCars if car.position[1] == os[0].position[1] + 1
                                       and car.position[0] >= ebLU
                                       and car.position[0] < os[len(os)-1].position[0] ]
        CRD = [car for car in tempCars if car.position[1] == os[0].position[1] - 1
                                       and car.position[0] <= ebRD
                                       and car.position[0] > os[len(os)-1].position[0] ]
        CLD = [car for car in tempCars if car.position[1] == os[0].position[1] - 1
                                       and car.position[0] >= ebLD
                                       and car.position[0] < os[len(os)-1].position[0] ]
        return (CRU, CLU, CRD, CLD)

##############################End GetCars related functions ###############################


##########################Costs #################################
    #Not the most foolproof getBestCS, so if it breaks don't be surprised :)
    def getBestCS(CS, os):
        csCosts = [costCS(cs, os) for cs in CS]
        return [cs for i, cs in enumerate(CS) if csCosts[i] == min(csCosts)][0]
    def costCar(car, op):
        a = params.turnTime ^ 2 
        b = params.laneVels[op.position[1]] - params.laneVels[car.position[1]]
        return car.priority * (car.accel - ( b / a ))
    
    def costCS(cs, os):
        for i, car in enumerate(cs):
            car.accel = generateAccel(car, os[i])

        return sum([costCar(car, op[i]) for i, car in enumerate(cars)])

    def generateAccel(car, op):
        x_f = op.position[0] * params.cellLength - car.position[0] * cellLength
        x_0 = 0
        v_0 = params.laneVels[car.position[1]]
        t = params.TurnTime
        accel = 2 * (x_f - v_0 * t) / (t^2)
        return accel

