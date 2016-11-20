# Autonomous Highway
This is the research code used in [Optimizing Departures of Automated Vehicles from Highways while Maintaining Mainline Capacity] (http://ieeexplore.ieee.org/document/7487015/)

Code in the how, when, do files make up the core 3 step process detailed in the paper.

The code that actually runs experiments is in tests.py.

To simply run the code and see the output logged in a *.p file do the following:

From a terminal:
```
$> python
from tests import *

p,s,a = runFlowSims(tests,100) # returns parameters of the run, all statistics of the run, and averages of those statistics
.
. (It will take some time to run. If you cancel the run early, no data will be saved (I know :( ))
.
> print a.g # Size ~11 - This will print the average EFR for flows in the order [0.5, 1.0, ..., 5.5] * 3,600 vehicles per lane. See the Statistics object in params.py for more detailed statistics. 
```
