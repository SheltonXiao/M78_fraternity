# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 13:39:00 2021

@author: asus
"""

#from PIL import Image

#img = Image.open("image/0702_3.png")
#print(img.size)
import matplotlib.pyplot as plt
import os
import cv2
from tqdm import trange
import math
import numpy as np

def cut(path,filename,typ):
    img = cv2.imread(path + "/"+ filename)
    
    subpath = path + "/subset"
    try:
        os.mkdir(subpath)
    except:
        pass
    
    rancol = int(img.shape[1]/20)
    ranrow = int(img.shape[0]/10)
    
    for i in trange(200):
        j = i + 200
        row = i // 20
        col = i % 20
        cropped = img[row*ranrow:(row+1)*ranrow, col*rancol:(col+1)*rancol]  # 裁剪坐标为[y0:y1, x0:x1]
        cv2.imwrite(subpath+"/"+str(j)+"_"+str(typ)+".png", cropped)
    

def fill(img,offset):
    cropped = img[offset:-offset+1, offset:-offset+1]
    top_size = offset
    bottom_size = offset
    left_size= int((cropped.shape[0] - cropped.shape[1])/2) + offset
    right_size = left_size
    
    constant=cv2.copyMakeBorder(cropped,top_size,bottom_size,left_size,right_size,
                                cv2.BORDER_CONSTANT,value=(255,255,255))
    return constant

path = "image"
#filename = "0702_3_2.png"
#cut(path,filename,1)
#filename = "0702_4_2.png"
#cut(path,filename,2)

offset = 20
for i in trange(400):
    j = i
    img1 = cv2.imread(path + "/subset/"+ str(j)+"_1.png")
    filled1 = fill(img1,offset)
    filled_resize1 = cv2.resize(filled1, dsize = (256, 256))
    """
    img2 = cv2.imread(path + "/subset/"+ str(j)+"_2.png")
    filled2 = fill(img2,offset)
    filled_resize2 = cv2.resize(filled2, dsize = (256, 256))
    rec = np.hstack((filled_resize1,filled_resize2))
    
    subpath = path + "/connect"
    try:
        os.mkdir(subpath)
    except:
        pass
    
    cv2.imwrite(subpath+"/"+str(j)+".png", rec)
    """
    subpath = path + "/cnn_input"
    try:
        os.mkdir(subpath)
    except:
        pass
    
    cv2.imwrite(subpath+"/"+str(j)+".png", filled_resize1)

"""    
#反色
#https://blog.csdn.net/yang__jing/article/details/89028060
for j in trange(400):
    img = cv2.imread("image/connect/"+ str(j)+".png")
    
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_white=np.array([0,0,221])
    upper_white=np.array([180,30,255])
    mask_white=cv2.inRange(hsv,lower_white,upper_white)
    
    lower_black=np.array([0,0,0])
    upper_black=np.array([180,255,46])
    mask_black=cv2.inRange(hsv,lower_black,upper_black)
    
    img_mask=np.copy(img)
    
    img_mask[mask_white!=0]=[0,0,0]
    img_mask[mask_black!=0]=[255,255,255]
    
    try:
        os.mkdir("image/black")
    except:
        pass
    
    cv2.imwrite("image/black/"+str(j)+".png", img_mask)
"""
    