import numpy as np
from utils import inBounds, countMissMatchedLabels

newR = [ 0, -1, -1, -1]
newC = [-1, -1,  0,  1]

def connectedComponentsIter(color_class=None, max_label=None):
    if(color_class is None):
        print('Error no color_class data')

    label         = 1 #start labeling from 1
    labels        = np.zeros(color_class.shape, np.int16)
    is_same_label = np.zeros(max_label  , np.int16)
    max_rows      = color_class.shape[0]
    max_cols      = color_class.shape[1]

    is_same_label.fill(10000)
    labels.fill(10000)

    #FIRST ITERATION
    for row in range(max_rows):
        for col in range(max_cols):
            foundMatch = False
            for k in range(3):
                nrow = row + newR[k]
                ncol = col + newC[k]
                if(inBounds(nrow,ncol,max_rows,max_cols)):
                        if(color_class[nrow,ncol] == color_class[row,col]):
                            if(foundMatch):
                                minLabel = min(labels[nrow,ncol], labels[row,col])
                                minLabel = min(minLabel, is_same_label[labels[nrow,ncol]])
                                minLabel = min(minLabel, is_same_label[labels[row,col]])
                                is_same_label[labels[row,col]] = minLabel
                                is_same_label[labels[nrow,ncol]] = minLabel
                            else:
                                labels[row,col] = labels[nrow,ncol]
                                foundMatch = True
            if(not foundMatch):
                labels[row,col] = label
                label = label + 1

    #SECOND ITERATION
    for row in range(max_rows):
        for col in range(max_cols):
            labels[row,col] = min(labels[row,col], is_same_label[labels[row,col]])
    return labels
