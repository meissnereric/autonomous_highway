from pylab import *
from tests import *

#data frame
testsNear = readFromFile("tests_far_linearCost_data.p")
baseNear = readFromFile("baseCaseTests_far_linearCost_data.p")
flows = [x * 0.5 for x in range(1,15)]
testColor = (0.5, 0.2, 0.2)
baseColor = (0.2, 0.2, 0.5)
numTurns = len(flows)
testNearG = []
baseNearG = []
for i in range(numTurns):
    testNearG.append( float(testsNear.numMissedCars[i]) / float(testsNear.numMadeCars[i]))
    baseNearG.append( float(baseNear.numMissedCars[i]) / float(baseNear.numMadeCars[i]))


figure(figsize=(10,7.5))

ax = subplot(111)
ax.spines["top"].set_visible(False)  
ax.spines["bottom"].set_visible(False)  
ax.spines["right"].set_visible(False)  
ax.spines["left"].set_visible(False)  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  
  
# Limit the range of the plot to only where the data is.  
# Avoid unnecessary whitespace.  
ylim(0, 0.2)  
xlim(0, 7.2)  
    
# Make sure your axis ticks are large enough to be easily read.  
# You don't want your viewers squinating to read your plot.  
yticks([0, 0.05, 0.1, 0.15, 0.2], [str(0) + "%", str(10) + "%", str(20) + "%", str(30) + "%", str(40) + "%", str(50) + "%",
    str(60) + "%", str(70) + "%"], fontsize=14)  
xticks(flows, [f * 3.6 for f in flows] , fontsize=14)  

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                        labelbottom="on", left="off", right="off", labelleft="on")  

plot(flows, testNearG, 'rs', label="Proposed")

plot(flows, baseNearG, 'b^',label="Naive")

text(3.5, 0.2, "Exit Failure Rate vs Flow (1,000 Cars/Hour/Lane)", fontsize=17, ha="center")

legend(bbox_to_anchor=(0.1, 0.9), loc=2,  borderaxespad=0., numpoints=1)

savefig("missedCars_flow.png", bbox_inches="tight");  




figure(figsize=(10,7.5))

ax = subplot(111)
ax.spines["top"].set_visible(False)  
ax.spines["bottom"].set_visible(False)  
ax.spines["right"].set_visible(False)  
ax.spines["left"].set_visible(False)  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  
  
# Limit the range of the plot to only where the data is.  
# Avoid unnecessary whitespace.  
ylim(0, 10)  
xlim(0, 7.2)  
    
# Make sure your axis ticks are large enough to be easily read.  
# You don't want your viewers squinting to read your plot.  
yticks([0,1,2,3,4], [0, str(1), str(2), str(3), str(4)], fontsize=14)  
xticks([f for f in flows], [f * 3.6 for f in flows] , fontsize=14)  

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                        labelbottom="on", left="off", right="off", labelleft="on")  

plot(flows, testsNear.turnTime, 'rs', label="Proposed")
plot(flows, baseNear.turnTime, 'b^',label="Naive")

text(3.5, 4.5, "Time To Compute 1 Turn (sec) vs Road Flow (1,000 Cars/Hour/Lane)", fontsize=17, ha="center")

legend(bbox_to_anchor=(0.1, 0.9), loc=2,  borderaxespad=0., numpoints=1)

savefig("timeToCompute_flow.png", bbox_inches="tight");  


figure(figsize=(10,7.5))

ax = subplot(111)
ax.spines["top"].set_visible(False)  
ax.spines["bottom"].set_visible(False)  
ax.spines["right"].set_visible(False)  
ax.spines["left"].set_visible(False)  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  
  
# Limit the range of the plot to only where the data is.  
# Avoid unnecessary whitespace.  
ylim(0, 5.2)  
xlim(0, 7.2)    
# Make sure your axis ticks are large enough to be easily read.  
# You don't want your viewers squinting to read your plot.  
yticks([0,1,2,3,4,5], [0, str(1), str(2), str(3), str(4), str(5)], fontsize=14)  
xticks(flows, [f * 3.6 for f in flows] , fontsize=14)  

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                        labelbottom="on", left="off", right="off", labelleft="on")  

plot(flows, testsNear.costPerLaneChange, 'rs', label="Proposed")

plot(flows, baseNear.costPerLaneChange, 'b^',label="Naive")

text(3.5, 5.2, "Cost Per Lane Change vs Road Flow (1,000 Cars/Hour/Lane)", fontsize=17, ha="center")

legend(bbox_to_anchor=(0.1, 0.9), loc=2,  borderaxespad=0., numpoints=1)

savefig("costs_flow.png", bbox_inches="tight");  
