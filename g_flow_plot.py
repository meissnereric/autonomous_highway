from pylab import *
from tests import *

#data frame
tests = readFromFile("tests_flow_0_7_data.p")
base = readFromFile("baseCaseTests_flow_0_7_data.p")
flows = [0.5, 1, 2, 3, 4, 5, 6, 7]
testColor = (25/255.0, 100/255.0, 25/255.0) 
baseColor = (25/255.0, 25/255.0, 100/255.0) 
numTurns = len(tests.numMissedCars)
testG = []
baseG = []
for i in range(numTurns):
    testG.append( float(tests.numMissedCars[i]) / float(tests.numMadeCars[i]))
    baseG.append( float(base.numMissedCars[i]) / float(base.numMadeCars[i]))

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
ylim(0, 0.3)  
xlim(0, 7)  
    
# Make sure your axis ticks are large enough to be easily read.  
# You don't want your viewers squinting to read your plot.  
yticks([0.05, 0.1, 0.15, 0.2, 0.25], [str(0.05) + "%", str(0.1) + "%", str(0.15) + "%", str(0.2) + "%", str(0.25) + "%"], fontsize=14)  
xticks(fontsize=14)  

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                        labelbottom="on", left="off", right="off", labelleft="on")  

plot(flows, testG, lw=2.5, color=testColor)
text(7.2, 0.05, "Test", fontsize=14, color=testColor)  

plot(flows, baseG, lw=2.5, color=baseColor)
text(7.2, 0.25, "Naive", fontsize=14, color=baseColor)  

text(3.5, 0.27, "Ratio of Cars Missing Their Exit Each Turn (G) vs Road Flow (Cars/Second/Lane)", fontsize=17, ha="center")

savefig("g_flow.png", bbox_inches="tight");  

