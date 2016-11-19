# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import matplotlib.pyplot as plt
#from matplotlib import rcParams
from tests import *

#rcParams['text.usetex'] = True

#alpha average g's across flows
#for i in range(0,9,1):
#    print np.mean(a.g[i*jump:(i+1)*jump])


p, s, a, _, _ = readAndAverage("tests_rAlpha_1.0-3.0_flow_0.5-5.5_1_18_2016_data.p")

alphas = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0]

figure = plt.figure(figsize=(10,7.5))

for flow in reversed(range(11)):
    plt.plot( alphas , [g for i,g in enumerate(a.g) if i % 11 == flow], label=str((flow+1)*0.5*3600))
plt.yticks(map(lambda x: x*0.01, xrange(10)), map(lambda x: str(x) + "%",xrange(10)), fontsize=14)  
plt.xticks(alphas, fontsize=14)  #ticks in cars/hour
plt.xlabel(' $ alpha $'+" Value")
plt.ylabel("Exit Failure Rate")
lgd = plt.legend()
lgd = plt.legend(bbox_to_anchor=(0.4, 0.9, .5, -0.25),
                   ncol=2, mode="expand", borderaxespad=0., title="Flow (Veh/Hr/Lane)")
plt.savefig("rAlpha_flow_g.png", bbox_extra_artists=(lgd,), bbox_inches='tight')

figure = plt.figure(figsize=(10,7.5))

plt.plot(a.g[2*11:3*11]) # rAlpha = 1.5 flows
plt.yticks(map(lambda x: x*0.01, xrange(1,8)), map(lambda x: str(x) + "%",xrange(1,8)), fontsize=14)  
plt.xticks(range(1,11,2),[(flow+1)*0.5*3600 for flow in range(1,11,2)])
plt.xlabel("Flow (Vehicles / Lane / Hour)")
plt.ylabel("Exit Failure Rate")
plt.savefig("alpha_1.5_g_flow.png")

figure = plt.figure(figsize=(10,7.5))

plt.plot(a.turnTime[2*11:3*11], label='Compute Time')
plt.plot([14.92]*len(a.turnTime[22:33]), label='Iteration Time T')
#plt.yticks(map(lambda x: x*0.01, xrange(1,8)), map(lambda x: str(x) + "%",xrange(1,8)), fontsize=14)  
plt.xticks(range(1,11,2),[(flow+1)*0.5*3600 for flow in range(1,11,2)])
plt.xlabel("Flow (Vehicles / Lane / Hour)")
plt.ylabel("Time Overhead (s)")
plt.savefig("alpha_1.5_turnTime_flow.png")

