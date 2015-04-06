
class RoadParameters:
    cellLength = 10.0 #in meters
    initLaneLength = 10 #in cells
    maxLaneLength = 40
    deltaVel = 5 #m/s
    maxAccel = 3 #m/s^2
    maxDecel = -3
    laneVels = [20.0,25.0,30.0,35.0,40.0]
    carsPerHour = 3600.0 #cars / hour
    flow = carsPerHour / 3600.0 #cars / second
    entrances = [6,16,26,36]
    exits = [10,20,30,40]
    percentContinuing = 0.5 #percentage of new cars on a road continuing
    maxEpsilonLook = 10
    turnTime = 10

    def laneCount():
        return len(self.velocities)

    def getPerSecondFlow():
        return perHourFlow / 3600

    def getPercentContinuing():
        return percentContinuing

    def getPercentEntering():
        return 1 - percentContinuing

params = RoadParameters()

class Statistics:
    lcCosts = []

stats = Statistics()
