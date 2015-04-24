from params import params

def do(PS): #[ (Platoon, op[] ) ]
    if len(PS) == 0:
        return []
    PS.sort(key = lambda p: p[0].priority)
    CLC = [] #cars actually lane changing
    CLC.append( PS.pop())
    while PS:

        v = PS.pop()
        # v =  (car, op)[] 
        if not inConflict(CLC, v):
            CLC.append(v)
    return CLC

def removeUniques(seq):
        seen = set()
        seen_add = seen.add
        return [ x for x in seq if not (x in seen or seen_add(x))]

#inconflict majorly uses lines 9-14 of Divya's algorithm 2
def inConflict(pls, v):
    #pls == [ (Platoon ,op[] ) ]
    # v = (Platoon, op[])

    #relevent cars
    rp = [pl for pl in pls if pl[0].position[1] == v[0].position[1] + 1
                                or pl[0].position[1] == v[0].position[1] + 2
                                or pl[0].position[1] == v[0].position[1] - 1
                                or pl[0].position[1] == v[0].position[1] - 2 ]
    (vx,vy) = v[0].position
    
    #pair = (Platoon, op[])
    for pair in rp:
        c = pair[0]
        # c = Platoon
        (cx,cy) = c.position
        if cx < vx:
            yi = vx*params.cellLength + params.laneVels[vy]*params.turnTime + v[0].accel * 0.5 * params.turnTime**2
            yj = cx*params.cellLength + params.laneVels[cy]*params.turnTime + c.accel * 0.5 * params.turnTime**2
        else:
            yj = vx*params.cellLength + params.laneVels[vy]*params.turnTime + v[0].accel * 0.5 * params.turnTime**2
            yi = cx*params.cellLength + params.laneVels[cy]*params.turnTime + c.accel * 0.5 * params.turnTime**2
        
        if yi > yj:
            ds = yi - c.length - yj
        else:
            ds = yj - c.length - yi

        if ds < 0:
            return True
    return False
