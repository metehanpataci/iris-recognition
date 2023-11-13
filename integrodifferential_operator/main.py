# -*- coding: utf-8 -*-

import thresh as thr
from PIL import Image
import os, os.path ,glob,sys
from skimage import io
import drawcircle as dc
import matplotlib.pyplot as plt
from skimage import img_as_float64
from skimage import img_as_float
import time
import datetime

# # #
# Function   :
# Parameters :
# Returns    :
# #
def read_all_eye_image_library(file_base_path): 
    imgs = []
    paths = []
    path = file_base_path
    valid_images = [".jpg",".gif",".png",".tga"]
    read_count = 0
    
    for root, subdirs, files in os.walk(path):
    
        for file in os.listdir(root):
    
            filePath = os.path.join(root, file)
    
            if os.path.isdir(filePath):
                pass
            else:
                ext = os.path.splitext(filePath)[1]
                
                if ext.lower() not in valid_images:
                    continue
                image = io.imread(filePath)
                imgs.append(image)
                paths.append(filePath)
                read_count = read_count + 1 
                
                #imgs.append(Image.open(os.path.join(filePath,f)))    
    return imgs,paths

def CURRENT_TIME():
    return datetime.datetime.now()

# # #
# Function   :
# Parameters :
# Returns    :
# #
def do_eye_detection(main_image_folder_path):
    print(CURRENT_TIME(),' Reading Images From ',main_image_folder_path,' ...')
    all_eye_images, image_paths = read_all_eye_image_library(main_image_folder_path)
    print(CURRENT_TIME()," All Images were readden..")
    print(CURRENT_TIME(),' Readden Image Count ',len(all_eye_images))
    
    element_cnt = len(all_eye_images)
    
    radius_min = 25
    radius_max = 80
    start_total_time = time.time()
    
    for i in range(element_cnt):
        print('* * * * * * * * * * * * * * * * * * * *')
        print(CURRENT_TIME(),' Process ',i)
        print(CURRENT_TIME(),' Eye Detection Strarted For ',image_paths[i])
        #print('* * * * * * * * * * * * * * * * * * * *')
        image = all_eye_images[i]
        start = time.time()
        thr.Thresh(image,radius_min,radius_max).thresh()
        end = time.time()
        print(CURRENT_TIME()," Detection Duration : ",end - start)
        print(CURRENT_TIME(),' Eye Detection Completed For ',image_paths[i])
        print('* * * * * * * * * * * * * * * * * * * *')
        print('')
        print('')
        print('')
            
    total_end = time.time()  
    total_time = total_end - start_total_time
    average_time = total_time / element_cnt
    print(CURRENT_TIME(),' Total Execution Time ms ',total_time)
    print(CURRENT_TIME(),' Average Detection Time ms: ',average_time)
            
# # #
# Function   :
# Parameters :
# Returns    :
# #
def main():
    print('Program Stared..')
    ##read all images
    do_eye_detection("UBIRIS_200_150_R/")
    
    

# # #
# Function   :
# Parameters :
# Returns    :
# #
main()
#read_all_eye_image_library()
#read_all2()


##############################################################################
############################ BACKUP ##########################################
##############################################################################

###
#
#
#
##
def read_all():
    root_dir = "UBIRIS_200_150_R/"

    for filename in glob.iglob(root_dir + '**/**', recursive=True):
        if os.path.isfile(filename):
            with open(filename,'r') as file:
                print(file.read())


###
#
#
#
##
def read_all_eye_image_library_old():
    imgs = []
    path = "UBIRIS_200_150_R/"
    valid_images = [".jpg",".gif",".png",".tga"]
    
    for f in os.listdir(path):
 
        ext = os.path.splitext(f)[1]
        print("exx",ext,f)
        if ext.lower() not in valid_images:
            continue
        print("Ext is ",ext)
        #imgs.append(Image.open(os.path.join(path,f))

    #return imgs                 