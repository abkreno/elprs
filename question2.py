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

def getSubImage(boundBox=None ,image=None, yUp=0, yDown=0):
    x = boundBox[0]
    y = boundBox[1] - yUp
    y = max(y,0)
    w = boundBox[2]
    h = boundBox[3] + yUp + yDown
    return image[y:y+h,x:x+w]

arabicAlphabet   = ('أ ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ى').split(" ")
image            = cv2.imread('library/arabic-digits.jpg')
digitsContours = getContours(image)
digitsImages   = []
for contour in digitsContours:
    sub_image        = getSubImage(cv2.boundingRect(contour),image)
    digitsImages.append(sub_image)
fig = plt.figure()
alphapetImages = []
#          ى   و   ه   ن   م   ل  ك   ق   ف  غ   ع   ظ  ط  ض  ص  ش  س   ز   ر   ذ   د   خ   ح   ج   ث   ت  ب   أ
yUps   = [ 0,  0, 15, 20,  0,  0, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
yDowns = [ 0, 15,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
count = 0
for i in range(4):
    path     = 'library/arabic-alphabet-'+str(i+1)+'.png'
    im       = cv2.imread(path)
    contours = getContours(im)
    for contour in contours:
        sub_image = getSubImage(cv2.boundingRect(contour),im,yUp=yUps[count],yDown=yDowns[count])
        alphapetImages.append(sub_image)
        count += 1
count = 1
for image in alphapetImages:
    fig.add_subplot(6,6,count)
    plt.imshow(image, cmap='gray')
    count+=1

plt.show()
