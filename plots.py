from pylab import *
from tests import *
import sys

print sys.argv

fileType = sys.argv[1]
fileName = "_er10_"+fileType+"_5_11_2015_data.p"

#data frame
(_, _, testsNormal) = readAndAverage("tests"+fileName)
(_, _, baseNormal) = readAndAverage("baseCaseTests"+fileName)

# testsNear = [stats(0.5), stats(1), stats(1.5), ..., stats(5.5)]
# avgTestsNear = [stats(avg(stats(0.5))), ..]

flows = [x * 0.5 for x in range(1,12)]
testColor = (0.5, 0.2, 0.2)
baseColor = (0.2, 0.2, 0.5)
numTurns = len(flows)
testNormalG = []
baseNormalG = []
for i in range(numTurns):
    testNormalG.append( float(testsNormal.numMissedCars[i]) / float(testsNormal.numMadeCars[i]))
    baseNormalG.append( float(baseNormal.numMissedCars[i]) / float(baseNormal.numMadeCars[i]))


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
ylim(0, 0.7)  
xlim(0, 6)  
    
# Make sure your axis ticks are large enough to be easily read.  
# You don't want your viewers squinating to read your plot.  
yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], [str(0) + "%", str(10) + "%", str(20) + "%", str(30) + "%", str(40) + "%",
    str(50)+ "%", str(60) + "%"], fontsize=14)  
xticks(flows, [f * 3.6 for f in flows] , fontsize=14)  #ticks in cars/hour

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                        labelbottom="on", left="off", right="off", labelleft="on")  

plot(flows, testNormalG, 'rs', label="Proposed")

plot(flows, baseNormalG, 'b^',label="Naive")

text(3, 0.65, "Exit Failure Rate vs Flow (1,000 Cars/Hour/Lane)", fontsize=17, ha="center")

legend(bbox_to_anchor=(0.1, 0.9), loc=2,  borderaxespad=0., numpoints=1)

savefig("missedCars_flow_"+fileType+".png", bbox_inches="tight");  




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
ylim(0, 25)  
xlim(0, 6)  
    
# Make sure your axis ticks are large enough to be easily read.  
# You don't want your viewers squinting to read your plot.  
yticks([0,5,10,15,20,25], [0, str(5), str(10), str(15), str(20), 25], fontsize=14)  
xticks([f for f in flows], [f * 3.6 for f in flows] , fontsize=14)  

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                        labelbottom="on", left="off", right="off", labelleft="on")  

plot(flows, testsNormal.turnTime, 'rs', label="Proposed")
plot(flows, baseNormal.turnTime, 'b^',label="Naive")

text(3, 26, "Time To Compute 1 Turn (sec) vs Road Flow (1,000 Cars/Hour/Lane)", fontsize=17, ha="center")

legend(bbox_to_anchor=(0.1, 0.9), loc=2,  borderaxespad=0., numpoints=1)

savefig("timeToCompute_flow_"+fileType+".png", bbox_inches="tight");  


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
ylim(0, 2)  
xlim(0, 6)    
# Make sure your axis ticks are large enough to be easily read.  
# You don't want your viewers squinting to read your plot.  
yticks([0,0.5, 1, 1.5], [0, str(0.5), 1, str(1.5)], fontsize=14)  
xticks(flows, [f * 3.6 for f in flows] , fontsize=14)  

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                        labelbottom="on", left="off", right="off", labelleft="on")  

plot(flows, testsNormal.costPerLaneChange, 'rs', label="Proposed")

plot(flows, baseNormal.costPerLaneChange, 'b^',label="Naive")

text(3, 2, "Cost Per Lane Change vs Road Flow (1,000 Cars/Hour/Lane)", fontsize=17, ha="center")

legend(bbox_to_anchor=(0.1, 0.9), loc=2,  borderaxespad=0., numpoints=1)

savefig("costs_flow_"+fileType+".png", bbox_inches="tight");  
