from pylab import *
from tests import *

#data frame
testsFar = readFromFile("tests_flow_0_7_far_data.p")
baseFar = readFromFile("baseCaseTests_flow_0_7_far_data.p")
testsNear = readFromFile("tests_flow_0_7_near_data.p")
baseNear = readFromFile("baseCaseTests_flow_0_7_near_data.p")
flows = [0.5, 1, 2, 3, 4, 5, 6, 7]
testColor = (0.5, 0.2, 0.2)
baseColor = (0.2, 0.2, 0.5)
numTurns = len(testsFar.numMissedCars)
testFarG = []
baseFarG = []
testNearG = []
baseNearG = []
for i in range(numTurns):
    testFarG.append( float(testsFar.numMissedCars[i]) / float(testsFar.numMadeCars[i]))
    baseFarG.append( float(baseFar.numMissedCars[i]) / float(baseFar.numMadeCars[i]))
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
ylim(0, 0.67)  
xlim(0, 7.2)  
    
# Make sure your axis ticks are large enough to be easily read.  
# You don't want your viewers squinting to read your plot.  
yticks([0.15, 0.3, 0.45, 0.6, 0.75], [str(15) + "%", str(30) + "%", str(45) + "%", str(60) + "%", str(75) + "%"], fontsize=14)  
xticks(fontsize=14)  

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                        labelbottom="on", left="off", right="off", labelleft="on")  

plot(flows, testFarG, 'rs')
text(7.2, 0.05, "Test Far", fontsize=14, color=testColor)  

plot(flows, baseFarG, 'bs')
text(7.2, 0.25, "Naive Far", fontsize=14, color=baseColor)  

plot(flows, testNearG, 'r^')
text(7.2, 0.63, "Test Near", fontsize=14, color=testColor)  

plot(flows, baseNearG, 'b^')
text(7.2, 0.15, "Naive Near", fontsize=14, color=baseColor)  

text(3.5, 0.7, "Ratio of Cars Missing Their Exit Each Turn (G) vs Road Flow (Cars/Second/Lane)", fontsize=17, ha="center")

savefig("missedCars_flow.png", bbox_inches="tight");  

