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
import search as src
import skimage as ski
from skimage import img_as_float64
from skimage import img_as_float
from skimage import img_as_ubyte
from skimage.transform import rescale
import partialid as part_id
import drawcircle as dc
import search as src
import scipy as sci
import scipy.ndimage as ndi
from skimage.morphology import reconstruction
import time
import datetime

#import scipy.ndimage.morphology.binary_fill_holes as binary_fill_holes

#function to search for the centre coordinates of the pupil and the iris
#along with their radii
#It makes use of Camus&Wildes' method to select the possible centre coordinates first
#The method consist of thresholding followed by
#checking if the selected points(by thresholding)
#correspond to a local minimum in their immediate(3*s) neighbourhood
#these points serve as the possible centre coordinates for the iris.
#Once the iris has been detected(using Daugman's method);the pupil's centre coordinates
#are found by searching a 10*10 neighbourhood around the iris centre and varying the radius
#until a maximum is found(using  Daugman's integrodifferential operator)
#INPUTS:
#I:image to be segmented
#rmin ,rmax:the minimum and maximum values of the iris radius
#OUTPUTS:
#cp:the parametrs[xc,yc,r] of the pupilary boundary
#ci:the parametrs[xc,yc,r] of the limbic boundary
#out:the segmented image
#Author:Anirudh S.K.
#Department of Computer Science and Engineering
#Indian Institute of Techology,Madras
class Thresh():
    # # #
    # Function   :
    # Parameters :
    # Returns    :
    # #
    def __init__(self,I,rmin,rmax):
        self.__I_matrix = I
        self.__radius_min = rmin
        self.__radius_max = rmax
    
    # # #
    # Function   :
    # Parameters :
    # Returns    :
    # #   
    def imcomplement(self,matrix_in):
        rows = matrix_in.shape[0]
        cols = matrix_in.shape[1]
        
        matrix_out = matrix_in.copy()
        
        for i in range(rows):
            for j in range(cols):
                matrix_out[i][j] = 1.0 - matrix_out[i][j]
    
        return matrix_out

    # # #
    # Function   :
    # Parameters :
    # Returns    :
    # #     
    def remove_elems_by_indexes(self,in_arr,remove_index_arr):
        elem_cnt = len(in_arr)
        remove_index_arr = np.array(remove_index_arr)
        remove_index_elem_cnt = remove_index_arr.shape[1]
        out_index = 0
        out = []
        found = False

        for i in range(elem_cnt):
            found = False
            for j in range(remove_index_elem_cnt):
                if i == remove_index_arr[0][j]:
                    found = True
                    break
            if found == False:
                out.append(in_arr[i])
                out_index = out_index + 1
            
        return out
    
    
    # # #
    # Function   :
    # Parameters :
    # Returns    :
    # #    
    def fill_holes_of_matrix(self,in_matrix):
        byte_matrix = img_as_ubyte(in_matrix)
        byte_matrix = 255 - byte_matrix
        seed = np.copy(byte_matrix)
        seed[1:-1, 1:-1] = byte_matrix.max()
        mask = byte_matrix
        Ifill = reconstruction(seed, byte_matrix, method='erosion')
        Ifill = Ifill.astype(dtype='uint8')
        byte_matrix = 255 - Ifill
        float_matrix = img_as_float64(byte_matrix)
        return float_matrix
    
    # # #
    # Function   :
    # Parameters :
    # Returns    :
    # #
    def thresh(self):
        I = self.__I_matrix
        rmin = self.__radius_min
        rmax = self.__radius_max
        scale = 1
        #Libor Masek's idea that reduces complexity
        #significantly by scaling down all images to a constant image size 
        #to speed up the whole process
        rmin = rmin * scale;
        rmax = rmax * scale;
        #scales all the parameters to the required scale
        #I = np. im2double(I); # 0.0 ve 1.0 araligina tasi
        I_uint8 = self.__I_matrix
        I = img_as_float64(self.__I_matrix)
        #arithmetic operations are not defined on uint8
        #hence the image is converted to double
        pimage = I;
        #stores the image for display
        I = rescale(I, scale)
        

        ## complement image
        
        #matlab  code
        #I = self.imcomplement(imfill(self.imcomplement(I),'holes'));# comp ile tersle imfill ile arada kalan yerleri 1 ile doldur. sonra tekrar tersle
        #I = self.imcomplement(sci.ndimage.binary_fill_holes(self.imcomplement(I)).astype(float))# comp ile tersle imfill ile arada kalan yerleri 1 ile doldur. sonra tekrar tersle
        
        I = self.fill_holes_of_matrix(I)
 
        
        #this process removes specular reflections by using the morphological operation 'imfill'
        #I=nbdavg(I);
        #blurs the sharp image formed as a result of using imfill
        rows = I.shape[0]
        cols = I.shape[1]
        
        [X,Y] = np.where(I < 0.5); # koyu yerleri belirle
        X = X.astype(float)
        Y = Y.astype(float)
        #Generates a column vector of the image elements
        #that have been selected by tresholding;one for x coordinate and one for y
        s = X.shape[0]
        
        for k in range(s): #
            if ( X[k] > rmin) & (Y[k] > rmin)&(X[k]<= (rows-rmin)) & (Y[k] < (cols-rmin)):
                
                A = I[(int(X[k])-1):(int(X[k])+1+1),(int(Y[k])-1):(int(Y[k])+1+1)]
                
                M = np.min(np.min(A))
                #this process scans the neighbourhood of the selected pixel
                #to check if it is a local minimum
                if I[int(X[k])][int(Y[k])] != M:
                    X[k]= np.NaN
                    Y[k]= np.NaN
           
        
        #Remove NaN values
          
        v = np.where(np.isnan(X));
        #X[v]=[]
        #Y[v]=[]
        
        X = X[~np.isnan(X)] 
        Y = Y[~np.isnan(Y)] 
        
        #deletes all pixels that are NOT local minima(that have been set to NaN)
        index = np.where((X<=rmin)|(Y<=rmin)|(X>(rows-rmin))|(Y>(cols-rmin)))
        X = np.array(self.remove_elems_by_indexes(X,index))
        Y = np.array(self.remove_elems_by_indexes(Y,index))
        #X[index]=[];
        #Y[index]=[];  
        
        #This process deletes all pixels that are so close to the border 
        #that they could not possibly be the centre coordinates.
        N = X.shape[0]
        #recompute the size after deleting unnecessary elements
        maxb = np.zeros([rows,cols]);
        maxrad = np.zeros([rows,cols]);
        #defines two arrays maxb and maxrad to store the maximum value of blur
        #for each of the selected centre points and the corresponding radius
        for j in range(N):
            [b,r,blur] =  part_id.PartialID(I,[X[j],Y[j]],rmin,rmax,'inf',600,'iris').partiald()#coarse search
            maxb[int(X[j])][int(Y[j])] = b
            maxrad[int(X[j])][int(Y[j])] = r
        
        x,y = np.where(maxb == np.max(np.max(maxb)));
        
        ci = src.Search(I,rmin,rmax,x,y,'iris').search()#fine search
        ci = np.array(ci)
        #finds the maximum value of blur by scanning all the centre coordinates
        ci = ci / scale;
        #the function search searches for the centre of the pupil and its radius
        #by scanning a 10*10 window around the iris centre for establishing 
        #the pupil's centre and hence its radius
        cp = src.Search(I,int(np.round(0.1 * r)),int(np.round(0.8*r)),int(ci[0] * scale),int(ci[1] * scale),'pupil').search()#Ref:Daugman's paper that sets biological limits on the relative sizes of the iris and pupil
        cp = np.array(cp)
        cp = cp/scale;
        
        print(datetime.datetime.now(),' Iris coordinate ',ci)
        print(datetime.datetime.now(),' Pupil coordinate ',cp)
        #displaying the segmented image
        #print('Iris Center:',ci[0],',',ci[1],' r:',ci[2])
        out = dc.DrawCircle(pimage,[int(ci[0]),int(ci[1])],int(ci[2]),600).drawcircle()
        #print('Pupil Center:',cp[0],',',cp[1],' r:',cp[2])
        out = dc.DrawCircle(out,[int(cp[0]),int(cp[1])],int(cp[2]),600).drawcircle()


        out = dc.DrawCircle(out,[int(cp[0]),int(cp[1])],int(cp[2]),600).drawcircle()
        plt.imshow(out,cmap='gray')
        plt.show()
        

# # # # # # # # # # # #
# # # # # # # # # # # #
# # # # TEST UTILITIES
# # # # # # # # # # # #
# # # # # # # # # # # #


"""
test = np.array([[0,1,1,0],[1,0,0,1],[0,1,1,0]])
print(test)
scipy.
binary_fill_holes(test)
"""