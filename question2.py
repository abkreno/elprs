import cv2
import numpy as np
from matplotlib import pyplot as plt
from utils import interHorz,findRectArea

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
        if(rect[2]>100):
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
    result = []
    boundingRects.sort(key=lambda tup: tup[0])
    for i in range(length):
        ind = boundingRects[i][4]
        if(not coveredRect[ind]):
            result.append(contours[ind])
    return result

# cnt = contours[4]
# cv2.drawContours(img, [cnt], 0, (0,255,0), 3)
im = cv2.imread('images/arabic-alphabet-4.png')
#x,y,w,h = 20,135,630,165
# CROPPING
#im = im[y:y+h,x:x+w]
contours = getContours(im)
cv2.drawContours(im, contours, 1, (0,255,0), 3)
plt.imshow(im, 'gray')
plt.show()
