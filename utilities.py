import rtc
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import argparse
from enum import Enum 
import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import numpy
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def plot_seaborn(array_counter, array_score):
    sns.set(color_codes=True)
    ax = sns.regplot(np.array([array_counter])[0], np.array([array_score])[0], color="b", x_jitter=.1, line_kws={'color':'green'})
    ax.set(xlabel='games', ylabel='score')
    plt.show()

# def get_unit_vector(p1, p2):
#     distance = Point(p2.x - p1.x, p2.y - p1.y)               #calculate vector between two points
#     norm = math.sqrt(distance.x ** 2 + distance.y ** 2)   #get magnitude of vector
#     direction = [distance.x / norm, distance.y / norm]    #normalize vector to unit vector
#     print(direction)    


def findCollisions(eng): 
    """Returns list of collisions of vehicles with other vehicles in list
    input -- vehicles_list: list of list of 4 points
    output -- list of points (collisions)
    """
    vehicles = eng.get_vehicle_corners()

    vehicle_list = []

    for vehicle in vehicles:
        vehicle_list.append([list(elem) for elem in vehicle])


    collisions_list = []

    for v in vehicle_list:
        for v2 in vehicle_list:
            if(v is not v2):
                if(do_polygons_intersect(v, v2)):
                    collisions_list.append([v, v2])

   
    # print(collisions_list)
    return collisions_list


    
def do_polygons_intersect(a, b):
    """
 * Helper function to determine whether there is an intersection between the two polygons described
 * by the lists of vertices. Uses the Separating Axis Theorem
 *
 * @param a an ndarray of connected points [[x_1, y_1], [x_2, y_2],...] that form a closed polygon
 * @param b an ndarray of connected points [[x_1, y_1], [x_2, y_2],...] that form a closed polygon
 * @return true if there is any intersection between the 2 polygons, false otherwise
    """

    polygons = [a, b];
    minA, maxA, projected, i, i1, j, minB, maxB = None, None, None, None, None, None, None, None

    for i in range(len(polygons)):

        # for each polygon, look at each edge of the polygon, and determine if it separates
        # the two shapes
        polygon = polygons[i];
        for i1 in range(len(polygon)):

            # grab 2 vertices to create an edge
            i2 = (i1 + 1) % len(polygon);
            p1 = polygon[i1];
            p2 = polygon[i2];

            # find the line perpendicular to this edge
            normal = { 'x': p2[1] - p1[1], 'y': p1[0] - p2[0] };

            minA, maxA = None, None
            # for each vertex in the first shape, project it onto the line perpendicular to the edge
            # and keep track of the min and max of these values
            for j in range(len(a)):
                projected = normal['x'] * a[j][0] + normal['y'] * a[j][1];
                if (minA is None) or (projected < minA): 
                    minA = projected

                if (maxA is None) or (projected > maxA):
                    maxA = projected

            # for each vertex in the second shape, project it onto the line perpendicular to the edge
            # and keep track of the min and max of these values
            minB, maxB = None, None
            for j in range(len(b)): 
                projected = normal['x'] * b[j][0] + normal['y'] * b[j][1]
                if (minB is None) or (projected < minB):
                    minB = projected

                if (maxB is None) or (projected > maxB):
                    maxB = projected

            # if there is no overlap between the projects, the edge we are looking at separates the two
            # polygons, and we know there is no overlap
            if (maxA < minB) or (maxB < minA):
                return False;

    # print("polygons intersect!")
    return True






  