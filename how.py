from params import params
import copy 

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
        if OS and OS[0] and OS[0][0].position[1] < params.numLanes-1:
            upCars = [car for car in road.cars if car.position[1] == OS[0][0].position[1]+1]
        else:
            upCars = []
        if OS and OS[0] and OS[0][0].position[1] > 0:

            downCars = [car for car in road.cars if car.position[1] == OS[0][0].position[1]-1]
        else:
            downCars = []
        for os in OS:
            (csUp, costUp) = getBestLaneCS(upCars, os, road.lanes[lane])#todo getCars + makeCS
            (csDown, costDown) = getBestLaneCS(downCars, os, road.lanes[lane])
            csUp = list(set(csUp))
            csDown = list(set(csDown))
            if len(csUp) == len(csDown):
                if costUp < costDown and maxCost > costUp > 0 and csUp:
                    realCars = getRealCars(upCars, csUp)
                    removeCS(upCars, realCars)
                    #print 'addFCS Up cuz costs: ' + str(costUp)
                    #printCS(realCars)
                    road.addFCS(realCars)
                elif csDown:
                    #print 'addFCS Down cuz costs' + str(costDown)
                    realCars = getRealCars(downCars, csDown)
                    removeCS(downCars, realCars)
                    #printCS(realCars)
                    road.addFCS(realCars)#todo don't add as platoon or only some
            else:
                if len(csUp) > len(csDown):
                    realCars = getRealCars(upCars, csUp)
                    #print 'addFCS Up due to length: ' + str(len(csUp))
                    removeCS(upCars, realCars)
                    #printCS(realCars)
                    road.addFCS(realCars)
                else:
                    realCars = getRealCars(downCars, csDown)
                    #print 'addFCS Down due to length: ' + str(len(csDown))
                    removeCS(downCars, realCars)
                    #printCS(realCars)
                    road.addFCS(realCars)#todo don't add as platoon or only some

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
    usedOps = []
    for pair in cs:
        if pair[0] in tempCars and pair[1] not in usedOps:
            tempCars.remove(pair[0])
            usedOps.append(pair[1])
        elif pair[0].accel < params.maxDecel or pair[0].accel > params.maxAccel or pair[1] in usedOps:
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
    (CR, CL) = doZPass(CR, CL, Z, os)
    for car in CR:
        if car.targetLane == car.position[1]:
            print 'whyyy are you still in CR!'
    for car in CL:
        if car.targetLane == car.position[1]:
            print 'whyyy are you still in CL!'
    CR.sort(key = lambda c: c.position[0]) #CR[0] is min X
    CL.sort(key = lambda c: c.position[0], reverse=True) #CL[0] is max X
    CR = list(set(CR))
    CL = list(set(CL))
    
    if CR or CL:
        #print 'os / CR / CL'
        s=""
        for op in os:
            s += str(op.position) + " "
        #print s
        s=""
        for car in CR:
            s += str(car.position) + " "
        #print s
        s=""
        for car in CL:
            s += str(car.position) + " "
        #print s
        #print ''

    bound = 0
    while (CR or CL) and len(CS) < len(os) and bound < len(cars) :
        bound += 1
        rCost = lCost = maxCost
        nrc = nlc = []
        rcs = lcs = []
        #print CR
        #print CL
        #print CS
        if CR:
            nrc = CR[0] #nearest right car
        if CL:
            nlc = CL[0] #left
        try:
            if nrc:
                if nrc.targetLane != os[0].position[1]:
                    print 'target lane of nrc not right'
                for cs in CS:
                    if nrc == cs[0]:
                        print 'force remove nrc'
                        CR.remove(nrc)
                        raise Exception('nlc','remove')
                op1 = os[0]
                op2 = os[len(os)-1]
                if op1.position[0] < op2.position[0]:
                    op = op2
                else:
                    op = op1
                (rcs, rCost) = costShift(CS, nrc, op, os, lane)
                if not rCost:
                    return (CS, costCSTotal(CS))
                #print 'rcs after costShift'
                #printCS(rcs)
                #print 'rCost: ' + str(rCost)
                #print 'len(rcs) immed. after costShift return: ' + str(len(rcs))
            if nlc:
                if nlc.targetLane != os[0].position[1]:
                    print 'target lane of nlc not right'
                for cs in CS:
                    if nlc == cs[0]:
                        print 'force remove nlc'
                        CL.remove(nlc)
                        raise Exception('nlc','remove')
                op1 = os[0]
                op2 = os[len(os)-1]
                if op1.position[0] > op2.position[0]:
                    op = op2
                else:
                    op = op1
                (lcs, lCost) = costShift(CS, nlc, op, os, lane)
                if not lCost:
                    return (CS, costCSTotal(CS))
               # print 'lcs after costShift'
               # printCS(lcs)
               # print 'lCost: ' + str(lCost)
               # print 'len(lcs) immed. after costShift return: ' + str(len(lcs))
        except Exception:
            continue
        

        if 0 <= rCost < lCost and rCost != maxCost and rcs:
            #print "len CS/rcs: " + str(len(CS)) + " : " + str(len(rcs))
            
            CS = rcs
            cost += rCost
            CR.remove(nrc)
            cars.remove(nrc)
        elif maxCost != lCost >= 0 and lcs:
           # print "len lcs: " + str(len(lcs))
            #print "len CS/lcs: " + str(len(CS)) + " : " + str(len(lcs))
            CS = lcs
            cost += lCost
            CL.remove(nlc)
            cars.remove(nlc)
        elif lCost == -1 or rCost == -1:
            s = ""
            for op in os:
                s += str(op.position) + " "
            #print s
            #print 'os full'
            break
        #print ''
    CS.sort(key = lambda pair: pair[1].position[0])
    #print "lenCS: " + str(len(CS)) + " cost: " + str(cost)
    #printCS(CS)
    #print ''
    return CS, costCSTotal(CS)

def costShift(CS, newCar, op, os, lane):
    #print 'CS coming into costShift'
    #printCS(CS)
    nCS = copy.copy(CS)
    right = left = False
    #first car - no blocking
    if not nCS or not nCS[0]:
        #print 'not CS'
        nCS.append( (newCar, op))
        return (nCS, costCS( (newCar, op) ))
   # print 'os bounds: ' + str(os[0].position) + " : " + str(os[len(os)-1].position)
   # print 'op: ' + str(op.position)
   # print 'car: ' + str(newCar)

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
    #    print 'right not blocked' + " " + str(currPos) + " " + str(op.position[0])
        return (nCS, costCS(nCS[-1]))
    elif currPos > op.position[0] and left:
        nCS.append( (newCar, op))
     #   print 'left not blocked' + " " + str(currPos) + " " + str(op.position[0])
        return (nCS, costCS(nCS[-1]))

    #check all the cars currently changing for placements
    elif right:
      #  print 'rightShift'
        rOp = getNearestOpening(nCS, os, left)
        if not rOp:
       #     print 'noOp'
            return(nCS, 0)
        shiftingCars = [pair for pair in nCS if pair[1].position[0] >= rOp.position[0]]
        notShiftingCars = [pair for pair in nCS if not (pair[1].position[0] >= rOp.position[0]) ]
        (shiftedCS, cost) = posShift(shiftingCars, newCar, op, lane)
        if not cost:
            return (CS, False)
       # print 'shifting cars:'
       # printCS(shiftingCars)
       # print 'not-shifting cars:'
       # printCS(notShiftingCars)
       # print 'shifted-cs :'
       # printCS(shiftedCS)
        nCS = notShiftingCars + shiftedCS
        nCS.append( (newCar, op))
        #print 'nCS at end of right shift'
        #printCS(nCS)
        return (nCS, cost)

    elif left:
        #print 'leftShift'
        lOp = getNearestOpening(nCS, os, left)
        if not lOp:
         #   print 'noOp'
            return(nCS, 0)
        shiftingCars = [pair for pair in nCS if pair[1].position[0] <= lOp.position[0]]
        notShiftingCars = [pair for pair in nCS if not (pair[1].position[0] <= lOp.position[0]) ]
        #print "1111 len ncs/shift/nShift: "
        #print str(len(nCS)) + " : " + str(len(shiftingCars)) + " : " + str(len(notShiftingCars))
        (shiftedCS, cost) = posShift(shiftingCars, newCar, op, lane)
        if not cost:
            return (CS, False)
        nCS = shiftedCS + notShiftingCars
        nCS.insert( 0, (newCar, op))
        #printCS(nCS)
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
    #print 'CS pre-posShift'
    #printCS(CS)
    ncs = []
    cost = 0
    #from the left
    if newCar.position[0] < op.position[0]:
      #  print 'cars shifting to the right'
        shift = 1
    else:
     #   print 'cars shifting to the left'
        shift = -1
    for cs in CS:
        newCell = lane.getCellByX(cs[1].position[0]+shift)
        if not newCell:
            return (CS, False)
        ncs.append( ( cs[0], newCell ) )
        if ncs[len(ncs)-1]:
            cost += costCS( ncs[len(ncs)-1] )
    #print 'CS post-posShift'
    #printCS(ncs)
    return (ncs, cost)

##########################Get Cars utilities  ########################################
def doEpsilonPass(tempCars, os):
    CR = [car for car in tempCars if car.position[0] < os[len(os)-1].position[0] + params.maxEpsilonLook
                    and car.position[0] > os[len(os)-1].position[0] ]

    CL = [car for car in tempCars if car.position[0] > os[0].position[0] - params.maxEpsilonLook
                                and car.position[0] < os[0].position[0] ]
    
    return (CR, CL)

def doZPass(CR, CL, z, os):
    
    if(len(CR) > z):
        CR = CR[0:z]
    if(len(CL) > z):
        CL = CL[len(CL) - z : len(CL)]

    CR = [car for car in CR if car.targetLane == os[0].position[1]]
    CL = [car for car in CL if car.targetLane == os[0].position[1]]
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
def costCS((car, op)):
    if car.accel == 0:
        car.accel = generateAccel(car, op)
    neededAccel = (params.laneVels[op.position[1]] - params.laneVels[car.position[1]]) / params.turnTime
    return abs(neededAccel - car.accel) ** 2

def costCSTotal(cs):
    if cs:
        return sum([costCS(pair) for pair in cs])
    else:
        return 1000000

#pg 136
def generateAccel(car, op):
    x_f = op.position[0] * params.cellLength
    x_0 = car.position[0] * params.cellLength
    v_d = params.laneVels[op.position[1]] - params.laneVels[car.position[1]]
    t = params.turnTime
    x_d = x_f - x_0
    accel = 2 * (x_d - v_d * t) / (t**2)
    return accel

def removeUniques(seq):
        seen = set()
        seen_add = seen.add
        return [ x for x in seq if not (x in seen or seen_add(x))]
