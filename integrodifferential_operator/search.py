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
import lineint as l_integral
from skimage import filters
import partialid as part_id
#function to detect the pupil  boundary
#it searches a certain subset of the image
#with a given radius range(rmin,rmax)
#around a 10*10 neighbourhood of the point x,y given as input
#INPUTS:
#im:image to be processed
#rmin:minimum radius
#rmax:maximum radius
#x:x-coordinate of centre point
#y:y-coordinate of centre point
#OUTPUT:
#cp:centre coordinates of pupil(x,y) followed by radius
#Author:Anirudh S.K.
#Department of Computer Science and Engineering
#Indian Institute of Techology,Madras
class Search():
    # # #
    # Function   :
    # Parameters :
    # Returns    :
    # #
    def __init__(self,im,rmin,rmax,x,y,option):
        self.__I_matrix = im
        self.__radius_min = rmin
        self.__radius_max = rmax
        self.__x_center = x
        self.__y_center = y
        self.part_name = option.lower()
        
    # # #
    # Function   :
    # Parameters :
    # Returns    :
    # #
    def search(self):
            rows = self.__I_matrix.shape[0]
            cols = self.__I_matrix.shape[1]
            
            sigma = 0.5;#(standard deviation of Gaussian)
            R = np.arange(self.__radius_min,self.__radius_max+1,1)
            maxrad = np.zeros([rows,cols])
            maxb = np.zeros([rows,cols])
            
            x_start = int((self.__x_center-5))
            x_end   = int(((self.__x_center+5)+1))
            
            y_start = int((self.__y_center-5))
            y_end   = int((self.__y_center+5+1))
            
            for i in range(x_start,x_end,1):
                for j in range(y_start,y_end,1):
                    [b,r,blur] = part_id.PartialID(self.__I_matrix,[i,j],self.__radius_min,self.__radius_max,0.5,600,self.part_name).partiald()
                    maxrad[i][j] = r
                    maxb[i][j] = b

            B = np.max(np.max(maxb))
            B_argmax = np.argmax(maxb)
            #X, Y = np.unravel_index(B_argmax, maxb.shape)
            X_ind_arr,Y_ind_arr = np.where(B == maxb)
            X = int(X_ind_arr)
            Y = int(Y_ind_arr)
            #[X,Y] = find(maxb==B)
            radius = maxrad[X][Y]
            cp = [X,Y,radius]
            return cp


