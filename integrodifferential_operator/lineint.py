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

#function to calculate the normalised line integral around a circular contour
#A polygon of large number of sides approximates a circle and hence is used
#here to calculate the line integral by summation
#INPUTS:
#1.I:Image to be processed
#2.C(x,y):Centre coordinates of the circumcircle
#Coordinate system :
#origin of coordinates is at the top left corner
#positive x axis points vertically down
#and positive y axis horizontally and to the right
#3.n:number of sides
#4.r:radius of circumcircle
#5.part:To indicate wheter search is for iris or pupil
#if the search is for the pupil,the function uses the entire circle(polygon) for computing L
#for the iris only the lateral portions are used to mitigate the effect of occlusions 
#that might occur at the top and/or at the bottom
#OUTPUT:
#L:the line integral divided by circumference

class LineIntegral():
    # # #
    # Function   :
    # Parameters :
    # Returns    :
    # #
    def __init__(self,I,C,r,n,part):
        self.__I_matrix = I
        self.__C_matrix = C
        self.__radius =r
        self.__number_of_sides = n
        self.part_of_pupil_name = part.lower()

    # # #
    # Function   :
    # Parameters :
    # Returns    :
    # #        
    def lineIntegral(self):
        
        theta = ((2.0 * np.pi) / self.__number_of_sides) # angle subtended at the centre by the sides
        #orient one of the radii to lie along the y axis
        #positive angle is ccw
        #Author:Anirudh S.K.
        #Department of Computer Science and Engineering
        #Indian Institute of Techology,Madras
        rows = self.__I_matrix.shape[0]
        cols = self.__I_matrix.shape[1]
        
        angle = np.arange(theta,((2.0 * np.pi) + theta),theta)
        
        x = self.__C_matrix[0] - (self.__radius * np.sin(angle))
        y = self.__C_matrix[1] + (self.__radius * np.cos(angle))
        
        L = 0
        
        if np.any(x >= rows) | np.any(y >= cols) | np.any( x <= 0) | np.any(y <= 0):
           L=0
           return L
        #This process returns L=0 for any circle that does not fit inside the image

        s = 0.0
        #lines 34 to 42 compute the whole line integral
        if self.part_of_pupil_name == 'pupil':
              s = 0.0
              for i in range(self.__number_of_sides):
                  val = self.__I_matrix[int(np.round(x[i]))][int(np.round(y[i]))]
                  s = s + val         
              L = s / self.__number_of_sides
    
        #lines 44 onwards compute the lateral line integral(to prevent occlusion affecting the results,the pixel average is taken only along the lateral portions)
        if self.part_of_pupil_name == 'iris':
            s=0;
            # slice 0 - n/8
            r1 = 0
            r2 = int(np.round(self.__number_of_sides / 8.0))
            for i in range(r2):
                val = self.__I_matrix[int(np.round(x[i]))][int(np.round(y[i]))];
                s=s+val;
          
            #slice (3 * n/8) - (5 * n / 8)
            r1 = int(np.round((3.0 * self.__number_of_sides) / 8.0))
            r2 = int(np.round((5.0 * self.__number_of_sides) / 8.0))
            for i in range(r1,(r2+1)):
                val = self.__I_matrix[int(np.round(x[i]))][int(np.round(y[i]))];
                s = s + val;
          
            r1 = int(np.round((7.0 * self.__number_of_sides) / 8.0))
            r2 = self.__number_of_sides
            for i in range(r1,(r2)):
                val = self.__I_matrix[int(np.round(x[i]))][int(np.round(y[i]))];
                s = s + val
           
            L = (2.0 * s) / float(self.__number_of_sides)
        
        return L

