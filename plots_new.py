from pylab import *
from tests import *

#Setup data
bp, bs, ba, _, _ = readAndAverage("baseCaseTests_pc02_flow_0.5-7.5_5_25_2015_data.p")
sp, ss, sa, _, _ = readAndAverage("tests_pc02_flow_0.5-7.5_5_25_2015_data.p")
lsp, lss, lsa, _, _ = readAndAverage("tests_cellLength12_flow_0.5-3.5_cellLength30_9_24_2015_data.p")


ba.g = [0]
sa.g = [0]
lsa.g = [0]
ba.turnTime.insert(0,0)
sa.turnTime.insert(0,0)
lsa.turnTime.insert(0,0)
print len(ba.numMissedCars)
for i, _ in enumerate(ba.numMissedCars):
    ba.g.append( ba.numMissedCars[i] / (ba.numMadeCars[i] + ba.numMissedCars[i]))
for i, _ in enumerate(sa.numMissedCars):
    sa.g.append( sa.numMissedCars[i] / (sa.numMadeCars[i] + sa.numMissedCars[i]))
for i, _ in enumerate(lsa.numMissedCars):
    lsa.g.append( lsa.numMissedCars[i] / (lsa.numMadeCars[i] + lsa.numMissedCars[i]))
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
ylim(0,0.15)
xlim(0,7.5)

yticks([0, 0.05, 0.1, 0.15], [ "", str(5) + "%", str(10) + "%", str(15) + "%"], fontsize=14)  
xticks(flowTicks, [f * 3.6 for f in flowTicks] , fontsize=14)  #ticks in cars/hour

plt.tick_params(axis="both", which="both", bottom="on", top="off",  
                        labelbottom="on", left="on", right="off", labelleft="on")  
bag_av = 0
sag_av = 0
lsag_av = 0
for i, _ in enumerate(ba.g):
    bag_av += ba.g[i]
    sag_av += sa.g[i]
for i, _ in enumerate(lsa.g):
    lsag_av += lsa.g[i]
bag_av = bag_av / len(ba.g)
sag_av = sag_av / len(sa.g)
lsag_av = lsag_av / len(lsa.g)

print len(lsa.g)
print len(sa.g)
while len(lsa.g) < len(sa.g):
    lsa.g.append(0)

#plot(flows, ba.g, label='Naive')
plot(flows, sa.g, label='Proposed')
text(-0.8, 0.135, "Exit Failure Rate", fontsize=14, ha="center")
text(3.55,-0.015, "Flow \n (x1000 Vehicles/Hour/Lane)", fontsize=14, ha="center")
legend(bbox_to_anchor=(0.1, 0.8), loc=2,  borderaxespad=0., numpoints=1)
savefig("flow_vs_g_10_11.png", bbox_inches="tight")

#Plot Flow vs Time Overhead
figure(figsize=(10,7.5))

ylim(0,15)
xlim(0,7.5)

yticks([0, 5, 10, 15], [ "", 5, str(10), str(15)], fontsize=14)  
xticks(flowTicks, [f * 3.6 for f in flowTicks] , fontsize=14)  #ticks in cars/hour

plt.tick_params(axis="both", which="both", bottom="on", top="off",  
                        labelbottom="on", left="on", right="off", labelleft="on")  

#bplot, = plot(flows, ba.turnTime, label='Naive')
splot, = plot(flows, sa.turnTime, label='Proposed')
plot(flows, [7.78]*len(sa.turnTime), label='Iteration Time T')
text(-0.95, 13, "Time Overhead (s)", fontsize=14, ha="center")
text(3.55, -2, "Flow \n (x1000 Vehicles/Hour/Lane)", fontsize=14, ha="center")
text(3.8, 8, "Iteration Time $T$", fontsize=14, ha="center")
legend(handles = [splot], bbox_to_anchor=(0.1, 0.8), loc=2,  borderaxespad=0., numpoints=1)
savefig("flow_vs_time_10_11.png", bbox_inches="tight")
