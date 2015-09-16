from pylab import *
from tests import *

#Setup data
bp, bs, ba, _, _ = readAndAverage("baseCaseTests_pc02_flow_0.5-7.5_5_25_2015_data.p")
sp, ss, sa, _, _ = readAndAverage("tests_pc02_flow_0.5-7.5_5_25_2015_data.p")

ba.g = [0]
sa.g = [0]
ba.turnTime.insert(0,0)
sa.turnTime.insert(0,0)
print len(ba.numMissedCars)
for i, _ in enumerate(ba.numMissedCars):
    ba.g.append( ba.numMissedCars[i] / ba.numMadeCars[i])
for i, _ in enumerate(sa.numMissedCars):
    sa.g.append( sa.numMissedCars[i] / sa.numMadeCars[i])
flows = [x * 0.5 for x in range(0,16)]
flowTicks = range(0,8)
#Pretty up the plot
testColor = (0.5, 0.2, 0.2)
baseColor = (0.2, 0.2, 0.5)

ax = subplot(111)
ax.spines["right"].set_visible(False)  
ax.spines["top"].set_visible(False)  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  


#Plot Flow vs G
figure(figsize=(10,7.5))
ylim(0,0.3)
xlim(0,7.5)

yticks([0, 0.05, 0.1, 0.15, 0.2, 0.25], [ "", str(5) + "%", str(10) + "%", str(15) + "%", str(20) + "%", str(25) + "%"], fontsize=14)  
xticks(flowTicks, [f * 3.6 for f in flowTicks] , fontsize=14)  #ticks in cars/hour

plt.tick_params(axis="both", which="both", bottom="on", top="off",  
                        labelbottom="on", left="on", right="off", labelleft="on")  

plot(flows, ba.g, label='Naive')
plot(flows, sa.g, label='Proposed')
text(3.75, 0.26, "Flow (1k Cars/Hour) vs Exit Success Rate", fontsize=14, ha="center")
legend(bbox_to_anchor=(0.1, 0.8), loc=2,  borderaxespad=0., numpoints=1)
savefig("flow_vs_g_5_29.png", bbox_inches="tight")

#Plot Flow vs Time Overhead
figure(figsize=(10,7.5))

ylim(0,25)
xlim(0,7.5)

yticks([0, 5, 10, 15, 20, 25], [ "", 5, str(10), str(15), str(20), str(25)], fontsize=14)  
xticks(flowTicks, [f * 3.6 for f in flowTicks] , fontsize=14)  #ticks in cars/hour

plt.tick_params(axis="both", which="both", bottom="on", top="off",  
                        labelbottom="on", left="on", right="off", labelleft="on")  

plot(flows, ba.turnTime, label='Naive')
plot(flows, sa.turnTime, label='Proposed')
plot(flows, [7.78]*len(sa.turnTime), label='Road Turn Time')
text(3.75, 22, "Flow (1k Cars/Hour) vs Time Overhead (s)", fontsize=14, ha="center")
legend(bbox_to_anchor=(0.1, 0.8), loc=2,  borderaxespad=0., numpoints=1)
savefig("flow_vs_time_5_29.png", bbox_inches="tight")
