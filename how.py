from params import params


def How(road):
    ActiveLanes = makeActiveLanes(road)
    tempCars = []
    if not ActiveLanes:
        return 
    ActiveLanes.sort()
    OS = getOpeningSets(ActiveLanes, road)
    OS.sort(key = lambda os: os[0].position[1], reverse=True)
    for y in range(len(params.laneVels)):
        tempCars = [car for car in road.cars if car.position[1] == y + 1
                                                or car.position[1] == y - 1]
        tempCars.sort(key = lambda c: c.position[0])
        for os in OS:
            if os[0].position[1] == y:
                os.sort(key = lambda op: op.position[0])
                (carsUp, carsDown) = getCars(tempCars, os)
                if carsUp:
                    carsUp.sort(key = lambda c: c.position[0])
                if carsDown:
                    carsDown.sort(key = lambda c: c.position[0])
                CS = makeCarSets(carsUp, os)
                CS.extend(makeCarSets(carsDown, os))
                CS = trimCS(CS)
                finalCS = getBestCS(CS)
                if finalCS:
                    road.addFCS(finalCS)
                    removeCars(tempCars, finalCS)

#should really only do things if len(os) > params.maxEpsilonLook
def trimCS(CS):
    for cs in CS:
        cars = cs[0]
        ops  = cs[1]
        for i in range(len(cars)):
            if abs(cars[i].position[0] - ops[i].position[0]) > params.maxEpsilonLook:
                CS.remove(cs)
                break
    return CS

#get OSs for a lane
def getOpeningSets(lane, road):
    OS = []
    os = []
    for i in range(len(road.lanes[lane].cells)):
        if (os) and (road.lanes[lane].cells[i].filled):
            OS.append(os)
            os = []
        elif not (road.lanes[lane].cells[i].filled):
            os.append(road.lanes[lane].cells[i])
    if os:
        OS.append(os)
    return OS
    

def removeCars(tempCars, cars):
    for car in cars:
        tempCars.remove(car)

def makeActiveLanes(road):
    ActiveLanes = []
    for car in road.cars:
        if(car.targetLane != car.position[1] and car.targetLane != -1):
            if not (car.targetLane in ActiveLanes):
                ActiveLanes.append(car.targetLane)
    return ActiveLanes

#def makeCarSets(cars, os):
 #   if not cars:
 #       return []
 #   CS = []
  #  cars.sort(key = lambda c: c.position[0])
   # os.sort(key = lambda c: c.position[0])
    #return possible subsets of cars filling the openings
  #  if len(os) < len(cars):
  #      for i in range(len(cars) - len(os)):
  #          pair = (cars[0+i : len(os) + i], os)
   #         CS.append( pair )
    #return car sets going to all possible contiguous combinations in the openings
    #elif len(os) == len(cars):
    #    CS.append( (cars,os))
    #else:
     #   for i in range(len(os) - len(cars)):
       #     pair = (cars, os[0+i : len(cars)+i])
       #     CS.append( pair )
   # return CS

#def sortCS(cs):
#if not cs:
#return 0
#    else:
#        cars = cs[0]
#        ops = cs[1]
#        return max([abs(car.position[0] - ops[i].position[0]) for i,car in enumerate(cars)])

def printCS(cs):
    cars = cs[0]
    ops = cs[1]
    #print ""
    #print "carLane : opLane -- " + str(cars[0].position[1]) + " : " + str(ops[0].position[1])
    s = ""
    if len(cars) != len(ops):
        print "cars != ops length"
    for i in range(len(cars)):
        s += (str(cars[i].position[0]) + " ")
    print s + " ***"
    s = ""
    for i in range(len(cars)):
        s += (str(ops[i].position[0]) + " ")
    print s

#4-16-15 changes to how
def newHow(road):
    ActiveLanes = makeActiveLanes(road)
    if not ActiveLanes:
        return
    ActiveLanes.sort()
    for lane in ActiveLanes:
        OS = getOpeningSets(lane, road)
        OS.sort(key = lambda os: os[0].position[0])
        upCars = []
        downCars = []
        for os in OS:
            (csUp, costUp) = getBestLaneCS(upCars, os, road.lanes[lane])#todo getCars + makeCS
            (csDown, costDown) = getBestLaneCS(downCars, os, road.lanes[lane])
            if costUp < costDown:
                road.addFCS(csUp)
                removeCars(upCars, csUp)
            else
                road.addFCS(csDown)#todo don't add as platoon or only some
               # removeCars(downCars, csDown)#todo generally remove cars


def getBestLaneCS(cars, os, lane):
    (blockUp, blockDown, zU, zD) = getBlockingSets(cars,os)
    
def getBlockingSets(cars, os):
    CS = []
    blockCars = [car for car in tempCars if car.position[0] <= os[len(os)-1].position[0]
                                        and car.position[0] >= os[0].position[0] ]
    Z = len(os) - len(blockCars)
    CS.append([ (car, lane.getCellByX(car.position[0])) for car in blockCars])#todo lane.getCellByX(x)
    removeCars(cars, blockCars)
    while cars and len(CS) < len(os):




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
    
   # print "TL: " + str(os[0].position[1]) + " blockUp : " + str(len(blockUp))
   # print "blockDown : " + str(len(blockDown))

    blockUp = [car for car in blockUp if car.targetLane == os[0].position[1]]
    blockDown = [car for car in blockDown if car.targetLane == os[0].position[1]]

    (CRU, CLU, CRD, CLD) = firstPassCars = doFirstPass(tempCars, os)
    (sRU, sLU, sRD, sLD) = SPC = doSecondPass(firstPassCars,os)
    (CRU, CLU, CRD, CLD) = finalCars = trimLengths(SPC, Z)

   # print "TL: " + str(os[0].position[1]) + " CRU/CLU/blockUp : " + str(len(CRU)) + " : " + str(len(CLU)) + " : " + str(len(blockUp))
    #print "CRD/CLD/blockDown : " + str(len(CRD)) + " : " + str(len(CLD)) + " : " + str(len(blockDown))
    #print ' '
    CU = [] 
    if blockUp:
        CU.extend(blockUp)
    if CRU:
        CU.extend(CRU)
    if CLU:
        CU.extend(CLU)

    CD = [] 
    if blockDown:
        CD.extend(blockDown)
    if CRD:
        CD.extend(CRD)
    if CLD:
        CD.extend(CLD)


        


    CU.sort(key= lambda c: c.position[0])
    CD.sort(key= lambda c: c.position[0])
        
    return (CU, CD)


def doFirstPass(tempCars, os):
    CRU = [car for car in tempCars if car.position[0] <= os[len(os)-1].position[0] + params.maxEpsilonLook
                                    and car.position[0] > os[len(os)-1].position[0] 
                                    and car.position[1] == os[0].position[1] + 1 ]

    CLU = [car for car in tempCars if car.position[0] >= os[0].position[0] - params.maxEpsilonLook
                                    and car.position[0] < os[0].position[0] 
                                    and car.position[1] == os[0].position[1] + 1 ]
    CRD = [car for car in tempCars if car.position[0] <= os[len(os)-1].position[0] + params.maxEpsilonLook
                                    and car.position[0] > os[len(os)-1].position[0] 
                                    and car.position[1] == os[0].position[1] - 1 ]

    CLD = [car for car in tempCars if car.position[0] >= os[0].position[0] - params.maxEpsilonLook
                                    and car.position[0] < os[0].position[0] 
                                    and car.position[1] == os[0].position[1] - 1 ]
    
    return (CRU, CLU, CRD, CLD)

def trimLengths((CRU, CLU, CRD, CLD), (z_u, z_d)):
    
    if(len(CRU) > z_u):
        CRU = CRU[0:z_u]
    if(len(CLU) > z_u):
        CLU = CLU[len(CLU) - z_u : len(CLU)]
    if(len(CRD) > z_d):
        CRD = CRD[0:z_d]
    if(len(CLD) > z_d):
        CLD = CLD[len(CLD) - z_d : len(CLD)]
    return (CRU, CLU, CRD, CLD)
    
#pg 108
def doSecondPass((fRU, fLU, fRD, fLD), os):
    
    ebRU = [car.position[0] for car in fRU if car.targetLane == car.position[1] ]
    if ebRU:
        ebRU = min(ebRU)
        sRU = [car for car in fRU if car.position[0] < ebRU]
    else:
        sRU = fRU

    ebLU = [car.position[0] for car in fLU if car.targetLane == car.position[1] ]
    if ebLU:
        ebLU = min(ebLU)
        sLU = [car for car in fLU if car.position[0] > ebLU]
    else:
        sLU = fLU

    ebRD = [car.position[0] for car in fRD if car.targetLane == car.position[1] ]
    if ebRD:
        ebRD = min(ebRD)
        sRD = [car for car in fRD if car.position[0] < ebRD]
    else:
        sRD = fRD

    ebLD = [car.position[0] for car in fLD if car.targetLane == car.position[1] ]
    if ebLD:
        ebLD = min(ebLD)
        sLD = [car for car in fLD if car.position[0] > ebLD]
    else:
        sLD = fLD



    return (sRU, sLU, sRD, sLD)
    
##############################End GetCars related functions ###############################


##########################Costs #################################
#Not the most foolproof getBestCS, so if it breaks don't be surprised :)
def getBestCS(CS):
    cutCS = [cs for cs in CS if cs != ([],[])]
    csCosts = [costCS(cs) for cs in cutCS]
    minCosts = [cs for i, cs in enumerate(cutCS) if csCosts[i] == min(csCosts)]
    if minCosts:
        return minCosts[0]
    else:
        return 
def costCar(car, op):
    a = params.turnTime ** 2 
    b = params.laneVels[op.position[1]] - params.laneVels[car.position[1]]
    return car.priority * (car.accel - ( b / a ))

def costCS(cs):
    for i, car in enumerate(cs[0]):
        car.accel = generateAccel(car, cs[1][i])

    return sum([costCar(car, cs[1][i]) for i, car in enumerate(cs[0])])

def generateAccel(car, op):
    x_f = op.position[0] * params.cellLength - car.position[0] * params.cellLength
    x_0 = 0
    v_0 = params.laneVels[car.position[1]]
    t = params.turnTime
    accel = 2 * (x_f - v_0 * t) / (t**2)
    return accel

def removeUniques(seq):
        seen = set()
        seen_add = seen.add
        return [ x for x in seq if not (x in seen or seen_add(x))]
