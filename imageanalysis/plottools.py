# encoding: utf-8

from matplotlib import pyplot as plt
import cv2


# plottikomento talteen

def plot_3histo(image):
    """Plot a three channel histo of an image with matplotlib

    :histo: TODO
    :returns: TODO

    """
    plt.figure()
    for i in range(0,3):
        histr = cv2.calcHist([tc],[i],None,[8],[0,256])
        plt.plot(histr)

