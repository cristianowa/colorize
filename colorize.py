#!/usr/bin/python
import sys
from opencvimage import CvImage
import math

def distance(a,b):
    x = pow(a[0] - b[0],2)
    y = pow(a[1] - b[1],2)
    z = pow(a[2] - b[2],2)
    return math.sqrt(x + y+ z)

def replacement(im_colors, colors):
    rep = {}
    for ic in im_colors:
        rep[ic] = None
        for c in colors:
            if rep[ic] == None:
                rep[ic] = c
            elif distance(ic,c) < distance(ic,rep[ic]):
                rep[ic] = c
    return rep

def colorize(imageName, colors, new_name=None):
    k = len(colors)
    im = CvImage.from_file(imageName)
    im.KMeansQuantization(k)
    im_colors = im.Colors()
    rep = replacement(im_colors, colors)
    im.Replace(rep)
    if new_name is None:
        new_name = imageName[:imageName.rfind(".")]
        new_name += "_colorized.jpg"
    im.Write(new_name)
    
if __name__ == "__main__":
    colors = [
    (191,154, 51),
    (212,214,177),
    (145,188,198),
    (  2, 71, 86),
    (  0, 20, 28)]
    for a in sys.argv[1:len(sys.argv)]:
        colorize(a, colors)
