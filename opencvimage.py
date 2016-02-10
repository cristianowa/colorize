#!/usr/bin/python
""" OpenCv Abstractions"""
import cv, cv2, time
from matplotlib import pyplot as plt
import numpy as np
from copy import copy
import Image
from matplotlib import cm


#enum HeatMapType 
class HeatMapType:
    """ HeatMapTypes"""
    Common = 0
    RedBLue = 1
    RedBlueFading = 2
    RedGreen = 3
    RedGreenFading = 4
    YellowBlue = 5
    YellowBlueFading = 6
    CyanRed = 7
    CyanRedFading = 8

class CvImage:
    """ OpenCv Image Abstraction """
    def __init__(self, original):

        if type(original) == type("string"):
            self.original = cv2.imread(original)
        else:
            self.original = original
        self.image = copy(self.original)
    @classmethod
    def from_file(cvImage, name):
        return cvImage(cv2.imread(name))
    @classmethod
    def from_image(cvImage, image):
        return cvImage(image)
    @classmethod
    def from_channels(cvImage, red=None, green=None, blue=None):
        if red == None and green == None: 
            raise Exception("merging in channels must have 2 or more images")
        if blue == None and red == None :
            raise Exception("merging in channels must have 2 or more images")
        if blue == None and green == None:
            raise Exception("merging in channels must have 2 or more images")
        if blue == None:
            blue = cvImage.from_image(np.zeros(red.Size(),dtype=np.uint8))
        if red == None:
            red = cvImage.from_image(np.zeros(blue.Size(),dtype=np.uint8))
        if green == None:
            green = cvImage.from_image(np.zeros(red.Size(),dtype=np.uint8))
        red.ToGray()
        blue.ToGray()
        green.ToGray()
        return cvImage.from_image(cv2.merge((red.image, green.image, blue.image)))
    def Size(self):
        return (len(self.image),len(self.image[0]))
    def Restore(self):
        self.image = copy(self.original)
    def Write(self, name):
        cv2.imwrite(name, self.image) 
    def __show__(self, image, name, x, y ):
        cv2.imshow(name, image)
        cv2.moveWindow(name, x, y)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    def Show(self, name = "Image", x = 10, y = 10):
        self.__show__(self.image, name, x, y)
    def KMeansQuantization(self, level = 4):
        img = copy(self.image)
        Z = img.reshape((-1,3))
        
        # convert to np.float32
        Z = np.float32(Z)
        
        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1)
        ret,label,center=cv2.kmeans(Z,level,criteria, 1,cv2.KMEANS_RANDOM_CENTERS)
        
        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        self.image = res.reshape((img.shape))
    def Colors(self):
        sz = self.Size()
        colors = []
        for x in range(sz[0]):
            for y in range(sz[1]):
                colors.append(tuple(self.image[x][y]))
        colors = list(set(colors))
        #colors = [ list(x) for x in colors]
        print colors
        return colors
    def Replace(self, rep):
        sz = self.Size()
        for x in range(sz[0]):
            for y in range(sz[1]):
                color = tuple(self.image[x][y])
                self.image[x][y] = np.array(rep[color], dtype=np.uint8)