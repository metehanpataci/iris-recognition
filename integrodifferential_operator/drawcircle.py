# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import data, exposure
from skimage.color import rgb2gray
from matplotlib import pyplot as plt
from skimage import data
from skimage.feature import corner_harris, corner_subpix, corner_peaks
from skimage.transform import warp, AffineTransform
from skimage.draw import ellipse
import numpy as np
from skimage.transform import hough_circle
from skimage.draw import circle_perimeter


###
#
#
#
##
class DrawCircle():
     
    # # #
    # Function   :
    # Parameters :
    # Returns    :
    # #
    def __init__(self,I,C,r,n):
        self.__I_matrix = I
        self.__C_coord = C
        self.__radius = r
        self.__number_of_sides = n
        self.__Out_matrix = self.__I_matrix.copy()

    # # #
    # Function   :
    # Parameters :
    # Returns    :
    # #
    def drawcircle(self):  
        theta = (2.0 * np.pi) / self.__number_of_sides # angle subtended at the centre by the sides
        # orient one of the radii to lie along the y axis
        # positive angle ic ccw
        rows = self.__I_matrix.shape[0]
        cols = self.__I_matrix.shape[1]
        angle = np.arange(theta,((2.0 * np.pi) + theta),theta)
        
        # to improve contrast and help in detection
        x = self.__C_coord[0] - (self.__radius * np.sin(angle)) # the negative sign occurs because of the particular choice of coordinate system
        y = self.__C_coord[1] + (self.__radius * np.cos(angle))
        
        if np.any(x >= rows) | np.any(y>=cols)| np.any(x<0)| np.any(y<0): #if circle is out of bounds return image itself
            self.__Out_matrix = self.__I_matrix
            return self.__Out_matrix
        
        out = self.__Out_matrix
        rr = range(0,(self.__number_of_sides))
        
        for i in range(0,(self.__number_of_sides)):
            self.__Out_matrix[int(np.round(x[i]))][int(np.round(y[i]))] = 1
    
        return self.__Out_matrix
    
    # # #
    # Function   :
    # Parameters :
    # Returns    :
    # #
    def drawcircleLib(self): 
        x = self.__C_coord[0]
        y = self.__C_coord[1]
        r =  self.__radius
        out = self.__Out_matrix 
        rr, cc = circle_perimeter(x,y,r)
        out[rr,cc] = 1.0
        return out 
    


def draw_circle_test():
    matrix = np.zeros([101,101])

    drawCirc = DrawCircle(matrix,[50,50],50,720) 

    plt.imshow(drawCirc.drawcircle(),cmap='gray')