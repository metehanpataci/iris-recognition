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

#function to find the partial derivative
#calculates the partial derivative of the normailzed line integral
#holding the centre coordinates constant
#and then smooths it by a gaussian of appropriate sigma 
##rmin and rmax are the minimum and maximum values of radii expected
#function also returns the maximum value of blur and the corresponding radius
#It also returns the finite differnce vector blur
#INPUTS:
#I;input image
#C:centre coordinates
#rmin,rmax:minimum and maximum radius values
#n:number of sides of the polygon(for lineint)
#part:specifies whether it is searching for the iris or pupil
#sigma:standard deviation of the gaussian
#OUTPUTS:
#blur:the finite differences vector
#r:radius at maximum value of 'blur'
#b:maximum value of 'blur'
#Author:Anirudh S.K.
#Department of Computer Science and Engineering
#Indian Institute of Techology,Madras


class PartialID():
        # # #
        # Function   :
        # Parameters :
        # Returns    :
        # #
        def __init__(self,I,C,rmin,rmax,sigma,n,part):
            self.__I_matrix = I
            self.__C_matrix = C
            self.__radius_min = rmin
            self.__radius_max = rmax
            self.__sigma = sigma
            self.__number_of_sides = n
            self.part_of_pupil_name = part.lower()
        
        # # #
        # Function   :
        # Parameters :
        # Returns    :
        # #
        def partiald(self):
            R = np.arange(self.__radius_min,self.__radius_max+1,1)
            
            count = R.shape[0]
            
            L = []
            
            for k in range(count):
                out = l_integral.LineIntegral(self.__I_matrix,self.__C_matrix ,R[k],self.__number_of_sides,self.part_of_pupil_name).lineIntegral()
                #[L[k]] = out
                if out == 0:#if L(k)==0(this case occurs iff the radius takes the circle out of the image)
                    #In this case,L is deleted as shown below and no more radii are taken for computation
                    #(for that particular centre point).This is accomplished using the break statement
                    #L[k]=[];
                    break
                L.append(out)
            
            L = np.array(L)    
            D = np.diff(L)
            D =np.insert(D,0,0)
            D = np.array(D)
            D = D.ravel()
            
            D_one_row = np.zeros([1,D.shape[0]])
            for i in range(D.shape[0]):
                D_one_row[0][i] = D[i]
            D_one_row = np.reshape(D_one_row,D.shape[0])
            #append one element at the beginning to make it an n vector
            #Partial derivative at rmin is assumed to be zero
            if self.__sigma == 'inf': #the limiting case of the gaussian with sigma infinity(pls remember to change the code)strcmp syntax is different
                f= np.ones([1,7]) / 7.0
                f = f.ravel()
                #f = np.reshape(f,5)
                #D_one_row = D_one_row.ravel()
                blur = np.convolve(D_one_row,f,'same')#Smooths the D vecor by 1-D convolution 
            else:
                #f = np.fspecial('gaussian',[1,5],sigma);#generates a 5 member 1-D gaussian
                #D_one_row = D_one_row.ravel()
                f = gauss1D_normalized(5,self.__sigma)
                f = np.reshape(f,(1,f.shape[0]))
                f = np.reshape(f,5)
                #blur = filters.gaussian(D_one_row, self.__sigma)
                blur = np.convolve(D_one_row,f,'same')#Smooths the D vecor by 1-D convolution 

            
            #blur = np.convolve(D,f,'same');#Smooths the D vecor by 1-D convolution 
            #'same' indicates that size(blur) equals size(D)
            blur = np.abs(blur).ravel()
            b = np.max(blur)
            i = np.argmax(blur)
            r = R[i]
            b = blur[i]
            return [b,r,blur]
            #calculates the blurred partial derivative


# *****************************************************************************
## Test Functions
# 
# *****************************************************************************
            
def fspecial_gauss(size, sigma):

    """Function to mimic the 'fspecial' gaussian MATLAB function
    """
    x, y = np.mgrid[-size//2 + 1:size//2 + 1, -size//2 + 1:size//2 + 1]
    g = np.exp(-((x**2 + y**2)/(2.0*sigma**2)))
    return g/g.sum()



def gauss1D(element_cnt,sigma):
    #-4 5
    elem = int(5/2)
    x = np.arange((-elem * 1),((elem+1) * 1),1.)#-2 * 1, 3*1
    kat = 1.0/ (sigma * np.sqrt((2.0 * np.pi)))
    k = kat * np.exp(-1.0 * ((x*x)/ (2.0 * sigma * sigma)))
    return k

def gauss1D_normalized(elem_cnt,sigma):
    g1d = gauss1D(elem_cnt,sigma)
    sum_g1d = np.sum(g1d)
    return g1d /sum_g1d

#def gaussian(x, mu, sig):
#    return np.exp(-np.power(x - mu, 2.) / (2.0 * np.power(sig, 2.)))* (1.0/ (sig * np.sqrt((2.0 * np.pi))))
def gaussian(x, mu, sig):
    return 1./(np.sqrt(2.*np.pi)*sig)*np.exp(-np.power((x - mu)/sig, 2.)/2)

def fgaussian(size, sigma):
     #m,n = size
     m = 1
     n = 5
     h, k = m//2, n//2
     x, y = np.mgrid[-h:h, -k:k]
     print(x)
     print(y)
     
     
#x = np.arange(1.)
#print(fgaussian(x,0.5))

#gau = gaussian(np.arange(-2,3,1.),0.0,0.5)
"""
gau = gauss1D(5,0.5)
print(gau)
tot = np.sum(gau)
print(tot)
print(gau/tot)
print('Gauss ',gauss1D_normalized(5,0.5))
"""
#print('Test 1 ',fspecial_gauss(2,0.5))
#print('test 2 ',fspecial_gauss(3,1))
#gauss1D(1)