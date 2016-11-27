# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt
from utils import interHorz,findRectArea,showImage,mse

def getContours(im=None):
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    boundingRects = []
    rectArea      = []
    length = len(contours)
    coveredRect = np.zeros((length), np.bool)
    for i in range(length):
        rect = cv2.boundingRect(contours[i])
        boundingRects.append(rect+(i,))
        rectArea.append(findRectArea(rect))
        if(rect[2]>im.shape[1]/2):
            coveredRect[i] = True

    for i in range(length):
        if(coveredRect[i]):
            continue
        for j in range(length):
            if(not coveredRect[j] and i != j and interHorz(boundingRects[i], boundingRects[j])):
                if(rectArea[i] <= rectArea[j]):
                    coveredRect[i] = True
                else:
                    coveredRect[j] = True
    res_contours = []
    # sort the bounding rectangles by left bound
    boundingRects.sort(key=lambda tup: tup[0])
    for i in range(length):
        ind = boundingRects[i][4]
        if(not coveredRect[ind]):
            res_contours.append(contours[ind])
    return res_contours

def getSubImage(boundBox=None ,image=None):
    x = boundBox[0]
    y = boundBox[1]
    w = boundBox[2]
    h = boundBox[3]
    return image[y:y+h,x:x+w]

arabicAlphabet   = ('أ ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ى').split(" ")
image            = cv2.imread('library/arabic-digits.jpg')
digitsContours = getContours(image)
alphapetContours = []
sub_image        = getSubImage(cv2.boundingRect(digitsContours[1]),image)
cv2.drawContours(image, digitsContours, 1, (0,255,0), 3)
showImage("Sub Image", sub_image)

# for i in range(4):
#     path     = 'library/arabic-alphabet-'+str(i+1)+'.png'
#     im       = cv2.imread(path)
#     contours,rects = getContours(im)
#     alphapetContours.append(contours)
#     alphapetRects.append(rects)
