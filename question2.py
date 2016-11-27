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

def getBestMatchIndex(input_image, boundingRect, subImage, arabicTemplates, yUps, yDowns):
    bestError,result,index = 1000000,0,0
    yUps = np.concatenate((np.zeros(10),yUps),axis=1)
    yDowns = np.concatenate((np.zeros(10),yDowns),axis=1)
    for image in arabicTemplates:
            subImage = getSubImage(boundingRect ,input_image,yUp=yUps[index],yDown=yDowns[index])
            subImage = cv2.cvtColor(subImage,cv2.COLOR_BGR2GRAY)
            height,width = subImage.shape
            image = cv2.resize(image,(width, height), interpolation = cv2.INTER_CUBIC)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            #ret,image = cv2.threshold(image,127,255,0)
            mseError = mse(subImage, image)
            if(mseError < bestError):
                bestError = mseError
                result = index
            index+=1
    return result

arabicAlphabet  = ('1 2 3 4 5 6 7 8 9 0 أ ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ى').split(" ")
arabicTemplates = []

arrow           = cv2.imread('images/arrow.jpeg')

image           = cv2.imread('library/arabic-digits.jpg')
digitsContours  = getContours(image)
count = 0
for contour in digitsContours:
    subImage        = getSubImage(cv2.boundingRect(contour),image)
    arabicTemplates.append(subImage)
    count+=1
    if(count>9):
        break
fig = plt.figure()

#          ى   و   ه   ن   م   ل  ك   ق   ف  غ   ع   ظ  ط  ض  ص  ش  س   ز   ر   ذ   د   خ   ح   ج   ث   ت  ب   أ
#          --------------------------------------------------------------------------------------------------------------
yUps   = [ 0,  0, 15, 20,  0,  0, 20,  0, 20,  0, 20,  0, 20,  0, 20,  0,  0,  0, 20, 20, 20, 20,  0,  0, 20,  0,  0,  0]
yDowns = [ 0, 15,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
count = 0
for i in range(4):
    path     = 'library/arabic-alphabet-'+str(i+1)+'.png'
    im       = cv2.imread(path)
    contours = getContours(im)
    for contour in contours:
        subImage = getSubImage(cv2.boundingRect(contour),im,yUp=yUps[count],yDown=yDowns[count])
        arabicTemplates.append(subImage)
        count += 1
# count = 1
# for image in arabicTemplates:
#     fig.add_subplot(6,7,count)
#     plt.axis("off")
#     plt.imshow(image, cmap='gray')
#     count+=1
# plt.show()
height = 325
width  = 669
#path = input("Enter the path to the image e.g \'images/L1.jpg\'\n\n")
input_image = cv2.imread('images/Test3.jpg')
input_image = cv2.resize(input_image,(width, height), interpolation = cv2.INTER_CUBIC)
input_image = np.concatenate((input_image[130:height-10,20:300],input_image[130:height-10,350:width-20]),axis=1)
input_contours = getContours(input_image)
count = 1

for contour in input_contours:
    boundingRect = cv2.boundingRect(contour)
    index     = getBestMatchIndex(input_image, boundingRect, subImage, arabicTemplates, yUps, yDowns)
    subImage = getSubImage(boundingRect ,input_image)
    print(arabicAlphabet[index])
    fig.add_subplot(8,3,count)
    plt.axis("off")
    plt.imshow(subImage, cmap='gray')
    count+=1
    fig.add_subplot(8,3,count)
    plt.axis("off")
    plt.imshow(arrow, cmap='gray')
    count+=1
    fig.add_subplot(8,3,count)
    plt.axis("off")
    plt.imshow(arabicTemplates[index], cmap='gray')
    count+=1
    if(count>24):
        break

plt.show()
