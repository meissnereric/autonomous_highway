import matplotlib.pyplot as plt
from tests import *

p, s, a, _, _ = readAndAverage("tests_k_thresh_10-30_flow_1.0-5.0_2_8_2016_data.p")
p1, s1, a1, _, _ = readAndAverage("tests_k_thresh_10-30_flow_6.0_2_8_2016_data.p")

kts = [10,15,20,25,30]

figure = plt.figure(figsize=(10,7.5))

plt.plot(kts, a1.g, label=str(6*3600))
for flow in reversed(range(len(a.g) / len(kts))):
    plt.plot( kts , [g for i,g in enumerate(a.g) if i % len(kts) == flow], label=str((flow+1)*3600))
plt.yticks(map(lambda x: x*0.01, xrange(10)), map(lambda x: str(x) + "%",xrange(10)), fontsize=14)  
plt.xticks(kts, fontsize=14)  #ticks in cars/hour
plt.xlabel("k_threshold Value")
plt.ylabel("Exit Failure Rate")
lgd = plt.legend(bbox_to_anchor=(0.25, 1, .5, -1.1),
                   ncol=2, mode="expand", borderaxespad=0., title="Flow (Veh/Hr/Lane)")
plt.savefig("kt_flow_g.png", bbox_extra_artists=(lgd,), bbox_inches='tight')


figure = plt.figure(figsize=(10,7.5))

p,s,a,mins,maxs = readAndAverage("tests_flow_0.5-6.0_2_8_2016_data.p")

print mins.g
print maxs.g

a.g.insert(0,0)
print a.g
print a.g[-1]
print len(a.g)
print a.turnTime[-1]
plt.plot([x * 0.5 for x in range(13)],a.g) # rAlpha = 1.5 flows
plt.yticks(map(lambda x: x*0.01, xrange(1,8)), map(lambda x: str(x) + "%",xrange(1,8)), fontsize=14)  
plt.xticks([x * 0.5 for x in range(0,13,2)],[(flow+1)*0.5*3600 -1800 for flow in range(0,13,2)])
plt.xlabel("Flow (Vehicles / Lane / Hour)")
plt.ylabel("Exit Failure Rate")
plt.savefig("flow_g_2-18-2016.png")
