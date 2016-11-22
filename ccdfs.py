import numpy as np
from utils import inBounds

newR = [ -1, -1, -1,  0,  0,  1,  1, 1]
newC = [ -1,  0,  1, -1,  1, -1,  0, 1]

def Dfs(row, col, color_class, labels, label):
    labels[row,col] = label
    for k in range(8):
        nrow = row + newR[k]
        ncol = col + newC[k]
        if(inBounds(nrow,ncol,color_class.shape[0],color_class.shape[1]) and labels[nrow,ncol] == 0 and color_class[nrow,ncol] == color_class[row,col]):
            Dfs(nrow, ncol, color_class, labels, label)

def connectedComponentsDfs(color_class=None, max_label=None):
    if(color_class is None):
        print('Error no color_class data')
    labels        = np.zeros(color_class.shape, np.int16)
    label         = 1 #start labeling from 1
    max_rows      = color_class.shape[0]
    max_cols      = color_class.shape[1]

    for row in range(max_rows):
        for col in range(max_cols):
            if(labels[row,col] == 0):
                Dfs(row,col,color_class,labels,label)
                label+=1
    return labels
