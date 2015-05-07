from params import params

def baseCaseHow(road):
    fcs = []
    OS = []
    for lane in makeActiveLanes(road):
        OS = getOpeningSets(road)
    for car in road.cars:
        if car.targetLane != car.position[1]:
            nop = getNearestOpening(car, OS, road.lanes[car.position[1]])
            if not nop:
                continue
            if abs(nop.position[0] - car.position[0]) <= params.maxEpsilonLook:
                OS.remove(nop)
                fcs.append( (car, nop))           
    road.addFCS( fcs )

def getNearestOpening(car, OS, lane):
    los = [op for op in OS if op.position[1] == car.targetLane]
    if not los:
        return
    dists = [ (abs(op.position[0] - car.position[0] ), op) for op in los]
    nearOp = min ( dists, key = lambda p: p[0] )
    return nearOp[1]

def makeActiveLanes(road):
    ActiveLanes = []
    for car in road.cars:
        if(car.targetLane != car.position[1] and car.targetLane != -1):
            if not (car.targetLane in ActiveLanes):
                ActiveLanes.append(car.targetLane)
    return ActiveLanes
def getOpeningSets(road):
    os = []
    for lane in range(len(road.lanes)):
        for i in range(len(road.lanes[lane].cells)):
            if not (road.lanes[lane].cells[i].filled):
                os.append(road.lanes[lane].cells[i])
    return os
