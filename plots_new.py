from pylab import *
from tests import *

bp, bs, ba = readAndAverage("baseCaseTests_uniform_percentCont_01-09_5_20_2015_data.p")
sp, ss, sa = readAndAverage("tests_uniform_percentCont_01-09_5_20_2015_data.p")

ba.g = []
sa.g = []
for i, _ in enumerate(ba.numMissedCars):
    ba.g.append( ba.numMissedCars[i] / ba.numMadeCars[i])
for i, _ in enumerate(sa.numMissedCars):
    sa.g.append( sa.numMissedCars[i] / sa.numMadeCars[i])
pc = [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1]

figure(figsize=(10,7.5))
ylim(0,0.6)
xlim(0,1.1)
plot(pc, ba.g, label='Naive')
plot(pc, sa.g, label='Proposed')
text(0.5, 0.55, "Percent Continuing vs Exit Success Rate at 20,000 Car/Hour", fontsize=14, ha="center")
legend(bbox_to_anchor=(0.1, 0.8), loc=2,  borderaxespad=0., numpoints=1)
savefig("pc_vs_g_5_23.png", bbox_inches="tight")


