import cv2
from random import randint
import numpy as np
from matplotlib import pyplot as pltd
from utils import inBounds, getColorClasses
from cciter import connectedComponentsIter
from ccdfs import connectedComponentsDfs

def showImage(title='Image', image=None):
    if(image is None):
        print('Error no image data')
        return
    cv2.imshow(title,image)
    cv2.waitKey(0)

def apply_label_colors(labels=None, colors=None, max_rows=None, max_cols=None):
        result_image = np.zeros((max_rows,max_cols,3), np.uint8)
        for row in range(max_rows):
            for col in range(max_cols):
                result_image[row,col] = colors[labels[row,col]%2000]
        return result_image

def generate_random_colors(limit=0):
    colors = []
    for i in range(limit):
        colors.append((randint(0,255),randint(0,255),randint(0,255)))
    return colors

img = cv2.imread('images/L1.jpg',0)
ret,thresh_image = cv2.threshold(img,127,255,cv2.THRESH_BINARY) #CONVERTING L1.jpg TO BINARY


#filling the image with colors according to labels
print(thresh_image)
print(getColorClasses(thresh_image))
#labels_dfs = connectedComponentsDfs(getColorClasses(thresh_image), 2000)
labels_iter = connectedComponentsIter(getColorClasses(thresh_image), 2000)

colors = generate_random_colors(2000)

max_rows      = thresh_image.shape[0]
max_cols      = thresh_image.shape[1]

result_image = apply_label_colors(labels_iter, colors, max_rows, max_cols)

showImage('Connected Components on Binary Image (DFS)', result_image)
