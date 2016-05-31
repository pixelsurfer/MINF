#Aufgabe 1

from PIL import Image
import numpy as np

import scipy.misc


def clean(pfad ,save):
    imageArray = Image.open(pfad)

    x, y = imageArray.size
    imageArray = np.array(imageArray)

    for i in range(y):
        for j in range(x):
            if imageArray[i][j][0] != imageArray[i][j][1] or imageArray[i][j][1] != imageArray[i][j][2]:
                imageArray[i][j][0] = imageArray[i][j-1][0]

    scipy.misc.imsave(save, np.array(imageArray[:,:,0], dtype=np.uint8))

clean("/Users/Trudi/Desktop/Hausarbeit/Hausarbeit/Aufgabe 1/poster_dirty.png", "/Users/Trudi/Desktop/clean11.png")




