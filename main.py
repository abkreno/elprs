import cv2
import numpy as np
from matplotlib import pyplot as plt
from utils import getColorClasses,applyLabelColors,generateRandomColors
from cciter import connectedComponentsIter
from ccdfs import connectedComponentsDfs

img = cv2.imread('images/L1.jpg',0)
ret,binary_image = cv2.threshold(img,127,255,cv2.THRESH_BINARY) #CONVERTING L1.jpg TO BINARY

img2 = cv2.imread('images/L3.jpg',0)

#filling the image with colors according to labels
#labels_dfs = connectedComponentsDfs(getColorClasses(binary_image), 2000)

max_rows      = img2.shape[0]
max_cols      = img2.shape[1]
max_label     = max_rows*max_cols
color_class   = getColorClasses(img2)
labels_iter   = connectedComponentsIter(color_class, max_label)
colors        = generateRandomColors(max_label)


result_image = applyLabelColors(labels_iter, colors, max_rows, max_cols)

#showImage('Connected Components on Binary Image (DFS)', result_image)
plt.imshow(result_image, 'BrBG')
plt.show()
