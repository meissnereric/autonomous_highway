from params import params

def do(CRLC): #(car, lc) tuples of cars requesting lane changes. From How
    if len(CRLC) == 0:
        return null
    CRLC = sortByPriority(CRLC)
    CALC = [] #cars actually lane changing
    CALC.append( CRLC.pop())
    while CRLC:
        v = CRLC.pop()
        if not inConflict(CALC, v):
            CALC.append(v)
    return CALC

#inconflict majorly uses lines 9-14 of Divya's algorithm 2
def inConflict(calc, v):
    #relevent cars
    rc = [car for car in calc if car.position[1] == v.position[1] + 1
                                or car.position[1] == v.position[1] + 2
                                or car.position[1] == v.position[1] - 1
                                or car.position[1] == v.position[1] - 2 ]
    (vx,vy) = v.position
    
    for c in rc:
        (cx,cy) = c.position
        if cx < vx:
            yi = vx + params.laneVels[vy]*params.TurnTime + v.accel * 0.5 * params.TurnTime^2
            yj = cx + params.laneVels[cy]*params.TurnTime + c.accel * 0.5 * params.TurnTime^2
        else:
            yj = vx + params.laneVels[vy]*params.TurnTime + v.accel * 0.5 * params.TurnTime^2
            yi = cx + params.laneVels[cy]*params.TurnTime + c.accel * 0.5 * params.TurnTime^2
        
        if yi > yj:
            ds = yi - params.cellLength - yj
        else:
            ds = yj - cellLength - yi

        if ds < 0:
            return true
    return false
