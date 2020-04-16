import rtc
# import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
import argparse
from enum import Enum 
import itertools
import matplotlib.pyplot as plt
# from mpl_toolkits.axes_grid1 import host_subplot
# import mpl_toolkits.axisartist as AA
import numpy
import math


from utilities import *

# fig = plt.figure()
# plt.xlabel('Width')
# plt.ylabel('Height')

eng = rtc.Engine("examples/config.json", thread_num=1)

score_plot = counter_plot = []

for i in range(40):
    eng.next_step()
    print("\n\n#############################")
    print("Step ", i+1)
    #print(eng.get_vehicle_corners())
    

    vehicles = eng.get_vehicle_corners()
    # findCollisions(vehicles)

    


# for i in range(len(vehicles)):
#     for j in range(4):
#         vehicles[i][j] = Point(vehicles[i][j][0], vehicles[i][j][1])



for vehicle in vehicles:    

    coordinates = []
    order = [0, 2, 3, 1, 0]
    for i in order:
        coordinates.append(vehicle[i])

    # xs, ys = zip(*coordinates)
    # plt.plot(xs, ys)
        


# plt.show()

#     counter_plot.append(0)

# 
# )

plot_seaborn([0, 0], [0, 0])   






