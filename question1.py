import cv2
import numpy as np
from matplotlib import pyplot as plt
from utils import getColorClasses,applyLabelColors,generateRandomColors
from cciter import connectedComponentsIter
from ccdfs import connectedComponentsDfs

img = cv2.imread('images/L1.jpg',0)
ret,binary_image = cv2.threshold(img,127,255,cv2.THRESH_BINARY) #CONVERTING L1.jpg TO BINARY

img2 = cv2.imread('images/L3.jpg',0)
#labels_dfs = connectedComponentsDfs(getColorClasses(binary_image), 2000)

max_rows      = img2.shape[0]
max_cols      = img2.shape[1]

# for himography transformation
src_pts       = np.float32([[5, 3],[998, 131],[925, 691],[66, 476]])
dst_pts       = np.float32([[0, 0],[max_cols-1, 0],[max_cols-1, max_rows-1],[0, max_rows-1]])
h_matrix,ret  = cv2.findHomography(src_pts,dst_pts)
fv_image      = cv2.warpPerspective(src=img2, M=h_matrix, dsize=(max_cols, max_rows))


max_label     = max_rows * max_cols
color_class   = getColorClasses(fv_image)
labels_iter   = connectedComponentsIter(color_class, max_label)
colors        = generateRandomColors(max_label)

result_image  = applyLabelColors(labels_iter, colors, max_rows, max_cols)

#showImage('Connected Components on Binary Image (DFS)', result_image)
plt.imshow(result_image, 'gray')
plt.show()
