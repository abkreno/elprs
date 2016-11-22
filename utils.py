newR = [ 0, -1, -1, -1]
newC = [-1, -1,  0,  1]

def inBounds(row=0, col=0, max_rows=0, max_cols=0):
    return row>=0 and row<max_rows and col >=0 and col < max_cols

def checkValid(image=None, labels=None):
    if(image is None or labels is None):
        print("inputs can't be none")
        return
    max_rows        = image.shape[0]
    max_cols        = image.shape[1]
    countNotMatched = 0
    for row in range(max_rows):
        for col in range(max_cols):
            for k in range(3):
                nrow = row + newR[k]
                ncol = col + newC[k]
                if(inBounds(nrow,ncol,max_rows,max_cols)):
                        if(image[nrow,ncol] == image[row,col] and labels[nrow,ncol] != labels[row,col]):
                            countNotMatched+=1
    return countNotMatched
