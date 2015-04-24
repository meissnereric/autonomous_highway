from params import params
import copy 

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

def removeCS(tempCars, cs):
    for pair in cs:
        if pair[0] in tempCars:
            tempCars.remove(pair[0])
        else:
            cs.remove(pair)
def makeActiveLanes(road):
    ActiveLanes = []
    for car in road.cars:
        if(car.targetLane != car.position[1] and car.targetLane != -1):
            if not (car.targetLane in ActiveLanes):
                ActiveLanes.append(car.targetLane)
    return ActiveLanes


def printCS(cs):
    cars = ops = ""
    for pair in cs:
        cars += (str(pair[0].position) + " ")
        ops += (str(pair[1].position) + " ")
    print cars
    print ops

#4-16-15 changes to how
# newHow 
def How(road):
    maxCost = 10000000
    ActiveLanes = makeActiveLanes(road)
    if not ActiveLanes:
        return
    ActiveLanes.sort()
    #print ActiveLanes
    for lane in ActiveLanes:
        OS = getOpeningSets(lane, road)
        OS.sort(key = lambda os: os[0].position[0])
        upCars = [car for car in road.cars if car.position[1] == OS[0][0].position[1]+1]
        downCars = [car for car in road.cars if car.position[1] == OS[0][0].position[1]-1]
        for os in OS:
            (csUp, costUp) = getBestLaneCS(upCars, os, road.lanes[lane])#todo getCars + makeCS
            (csDown, costDown) = getBestLaneCS(downCars, os, road.lanes[lane])
            csUp = list(set(csUp))
            csDown = list(set(csDown))
            if len(csUp) == len(csDown):
                if costUp < costDown and maxCost > costUp > 0 and csUp:
                    realCars = getRealCars(upCars, csUp)
                    removeCS(upCars, realCars)
                    print 'addFCS Up cuz costs: ' + str(costUp)
                    printCS(realCars)
                    road.addFCS(realCars)
                elif csDown:
                    print 'addFCS Down cuz costs' + str(costDown)
                    realCars = getRealCars(downCars, csDown)
                    removeCS(downCars, realCars)
                    printCS(realCars)
                    road.addFCS(realCars)#todo don't add as platoon or only some
            else:
                if len(csUp) > len(csDown):
                    realCars = getRealCars(upCars, csUp)
                    print 'addFCS Up due to length: ' + str(len(csUp))
                    removeCS(upCars, realCars)
                    printCS(realCars)
                    road.addFCS(realCars)
                else:
                    realCars = getRealCars(downCars, csDown)
                    print 'addFCS Down due to length: ' + str(len(csDown))
                    removeCS(downCars, realCars)
                    printCS(realCars)
                    road.addFCS(realCars)#todo don't add as platoon or only some

def getRealCars(real, fake):
    realCS = []
    for pair in fake:
        for car in real:
            if car.position == pair[0].position:
                realCS.append( (car, pair[1]))
                break
    return realCS

def getBestLaneCS(permCars, os, lane):
    cars = copy.copy(permCars)
    maxCost = 10000000
    if not cars:
        return ([], maxCost)
    CS = []
    cost = 0.0
    blockCars = [car for car in cars if car.position[0] <= os[len(os)-1].position[0]
                                        and car.position[0] >= os[0].position[0] ]
    Z = len(os) - len(blockCars)
    blockCars = [car for car in blockCars if car.targetLane == os[0].position[1]]
    
    #todo update blockCar costs and maybe add the cars to their "safe zone" spots when able
    bcCS = [ (car, lane.getCellByX(car.position[0])) for car in blockCars]
    
    for cs in bcCS:
        CS.append(cs)
    
    removeCars(cars, blockCars)
    (CR, CL) = doEpsilonPass(cars, os)
    (CR,CL) = doEBPass(CR, CL, os)
    (CR, CL) = doZPass(CR, CL, os)
    CR.sort(key = lambda c: c.position[0]) #CR[0] is min X
    CL.sort(key = lambda c: c.position[0], reverse=True) #CL[0] is max X
    

    bound = 0
    while (CR or CL) and len(CS) < len(os) and bound < len(cars) :
        bound += 1
        rCost = lCost = maxCost
        nrc = nlc = []
        rcs = lcs = []
        if CR:
            nrc = CR[0] #nearest right car
        if CL:
            nlc = CL[0] #left

        if nrc:
            (rcs, rCost) = costShift(CS, nrc, os[len(os)-1], os, lane)
     #       print 'rCost: ' + str(rCost)
      #      print 'len(rcs) immed. after costShift return: ' + str(len(rcs))
        if nlc:
            (lcs, lCost) = costShift(CS, nlc, os[0], os, lane)
       #     print 'lCost: ' + str(lCost)
        #    print 'len(lcs) immed. after costShift return: ' + str(len(lcs))

        

        if 0 <= rCost < lCost and rCost != maxCost and rcs:
         #   print "len CS/rcs: " + str(len(CS)) + " : " + str(len(rcs))
            
            CS = rcs
            cost += rCost
            CR.remove(nrc)
            cars.remove(nrc)
        elif maxCost != lCost >= 0 and lcs:
           # print "len lcs: " + str(len(lcs))
          #  print "len CS/lcs: " + str(len(CS)) + " : " + str(len(lcs))
            CS = lcs
            cost += lCost
            CL.remove(nlc)
            cars.remove(nlc)
        elif lCost == -1 or rCost == -1:
            s = ""
            for op in os:
                s += str(op.position) + " "
            #print s
           # print 'os full'
            break

    #print "lenCS: " + str(len(CS)) + " cost: " + str(cost)
    #printCS(CS)
    #print ''
    return CS, cost

def costShift(CS, newCar, op, os, lane):
    nCS = CS
    right = left = False
    #first car - no blocking
    if not nCS or not nCS[0]:
        #print 'not CS'
        nCS.append( (newCar, op))
        return (nCS, costCS( (newCar, op) ))

    #car from the right
    if newCar.position[0] > op.position[0]:
        nCS.sort(key = lambda cs: cs[1].position[0])
        right = True
    else: #left
        nCS.sort(key = lambda cs: cs[1].position[0], reverse=True)
        left = True

    prevPos = 0
    currPos = nCS[-1][1].position[0] #[0] -> first pair , [1] opening of it
    if currPos < op.position[0] and right:
        nCS.append( (newCar, op))
        #print 'right not blocked' + " " + str(currPos) + " " + str(op.position[0])
        return (nCS, costCS(nCS[-1]))
    elif currPos > op.position[0] and left:
        nCS.append( (newCar, op))
        #print 'left not blocked' + " " + str(currPos) + " " + str(op.position[0])
        return (nCS, costCS(nCS[-1]))

    #check all the cars currently changing for placements
    elif right:
        #print 'rightShift'
        rOp = getNearestOpening(nCS, os, left)
        if not rOp:
            #print 'noOp'
            return(nCS, 0)
        shiftingCars = [pair for pair in nCS if pair[1].position[0] > rOp.position[0]]
        notShiftingCars = [pair for pair in nCS if not (pair[1].position[0] > rOp.position[0]) ]
        #print "1111 len ncs/shift/nShift: "
        #print str(len(nCS)) + " : " + str(len(shiftingCars)) + " : " + str(len(notShiftingCars))
        (shiftedCS, cost) = posShift(shiftingCars, newCar, op, lane)
        nCS = notShiftingCars + shiftedCS
        nCS.append( (newCar, op))
        return (nCS, cost)

    elif left:
        #print 'leftShift'
        lOp = getNearestOpening(nCS, os, left)
        if not lOp:
          #  print 'noOp'
            return(nCS, 0)
        shiftingCars = [pair for pair in nCS if pair[1].position[0] < lOp.position[0]]
        notShiftingCars = [pair for pair in nCS if not (pair[1].position[0] < lOp.position[0]) ]
       # print "1111 len ncs/shift/nShift: "
       # print str(len(nCS)) + " : " + str(len(shiftingCars)) + " : " + str(len(notShiftingCars))
        (shiftedCS, cost) = posShift(shiftingCars, newCar, op, lane)
        nCS = shiftedCS + notShiftingCars
        nCS.insert( 0, (newCar, op))
        return (nCS, cost)

   # print '-1'
    return (nCS, -1)
    
#page 135
def getNearestOpening(CS, os, left):
    #print "len(CS) in getNearOp: "+ str( len(CS))
    #print "len(os) in getNearOp: "+ str( len(os))
    if left:
        CS.sort(key = lambda cs: cs[1].position[0])
        os.sort(key = lambda op: op.position[0])
    else: #right
        CS.sort(key = lambda cs: cs[1].position[0], reverse=True)
        os.sort(key = lambda op: op.position[0], reverse=True)

    pairings = []
    contiguous = []
    for i in range(len(os)):
        if i < len(CS):
            pairings.append((CS[i], os[i]))
        else:
            contiguous.append( os[i])
    

    disjointPairings = [p for p in pairings if p[0][1].position[0] != p[1].position[0] ]  
    if disjointPairings: #there is an opening
        if disjointPairings[0][0][1].position[0] <= contiguous[0].position[0]:
            return disjointPairings[0][0][1]
        else:
            return contiguous[0]
    elif contiguous:
        return contiguous[0]
    else: #no openings
        return

def posShift(CS, newCar, op, lane):
    ncs = []
    cost = 0
    #from the left
    if newCar.position[0] < op.position[0]:
        shift = 1
    else:
        shift = -1
    for cs in CS:
        newCell = lane.getCellByX(cs[1].position[0]+shift)
        ncs.append( ( cs[0], newCell ) )
        if ncs[len(ncs)-1]:
            cost += costCS( ncs[len(ncs)-1] )
    return (ncs, cost)

##########################Get Cars utilities  ########################################
def doEpsilonPass(tempCars, os):
    CR = [car for car in tempCars if car.position[0] <= os[len(os)-1].position[0] + params.maxEpsilonLook
                    and car.targetLane == os[0].position[1]                
                    and car.position[0] > os[len(os)-1].position[0] ]

    CL = [car for car in tempCars if car.position[0] >= os[0].position[0] - params.maxEpsilonLook
                                and car.targetLane == os[0].position[1]                
                                and car.position[0] < os[0].position[0] ]
    
    return (CR, CL)

def doZPass(CR, CL, z):
    
    if(len(CR) > z):
        CR = CR[0:z]
    if(len(CL) > z):
        CL = CL[len(CL) - z : len(CL)]
    return (CR, CL)

#pg 108
def doEBPass(fR, fL, os):
    
    ebR = [car.position[0] for car in fR if car.targetLane == car.position[1] ]
    if ebR:
        ebR = min(ebR)
        sR = [car for car in fR if car.position[0] < ebR]
    else:
        sR = fR

    ebL = [car.position[0] for car in fL if car.targetLane == car.position[1] ]
    if ebL:
        ebL = min(ebL)
        sL = [car for car in fL if car.position[0] > ebL]
    else:
        sL = fL



    return (sR, sL)
    
##############################End GetCars related functions ###############################


##########################Costs #################################
#Not the most foolproof getBestCS, so if it breaks don't be surprised :)
#def getBestCS(CS):
#    cutCS = [cs for cs in CS if cs != ([],[])]
#    csCosts = [costCS(cs) for cs in cutCS]
#    minCosts = [cs for i, cs in enumerate(cutCS) if csCosts[i] == min(csCosts)]
#    if minCosts:
#        return minCosts[0]
#    else:
#        return 
def costCS((car, op)):
    car.accel = generateAccel(car, op)
    t = params.turnTime ** 2 
    d_v = params.deltaVel
    return car.priority * abs((car.accel - ( d_v / t )) ** 2)

def costCSTotal(cs):
    for i, car in enumerate(cs[0]):
        car.accel = generateAccel(car, cs[1][i])

    return sum([costCar(car, cs[1][i]) for i, car in enumerate(cs[0])])

#pg 136
def generateAccel(car, op):
    x_f = op.position[0] * params.cellLength
    x_0 = car.position[0] * params.cellLength
    v_d = params.laneVels[car.position[1]] - params.laneVels[op.position[1]]
    t = params.turnTime
    accel = 2 * (x_f - x_0 - v_d * t) / (t**2)
    if accel > params.maxAccel or accel < params.maxDecel:
        print "accel -- " + str(accel) 
    return accel

def removeUniques(seq):
        seen = set()
        seen_add = seen.add
        return [ x for x in seq if not (x in seen or seen_add(x))]
