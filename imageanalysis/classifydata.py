# encoding: utf-8

# script: classify text / image clippings with historgram info
import os
import numpy as np
import cv2
import pickle
import re

# helpers:

# TODO these two really should be moved into a module!

def calc_hist(clip):
    return cv2.calcHist([clip], [0,1,2], None, [8,8,8], [0, 256, 0,256, 0,256])


def process_clipfiles(dirname):
    dirlist = os.listdir(dirname)
    flathists = []
    clipnames = []
    images = []
    clipsizes = []
    for clip_name in dirlist:
        clip_image = cv2.imread(dirname + clip_name)
        images.append(clip_image)
        # when we're at it, we can also get their sizes:
        clipsizes.append(clip_image.size)
        # for coordinates we need version of createtraindataclips.py that saves them, too >.>
        # TODO ^ also modify to get rid of alpha channel

        hist3c = calc_hist(clip_image)
        hist_flat = hist3c.flatten()
        flathists.append(hist_flat)
        clipnames.append(clip_name)

    return flathists, clipnames, images, clipsizes

def numpyfy_clipnames(clipnames):
    # clipnames a python list!
    # clipname format "bw-yyyy-nn-pppp.png-clip-c.png" (ew that's ugly)
    # because substr 'c' (clip no) isn't fixed width ( >.> ),
    # I guess the fastest way is even uglier regex
    rep = re.compile(r"bw-(\d{4})-(\d{2})-(\d{4})\.png-clip-(\d+)\.png")
    cliparr = np.zeros((len(clipnames), 4), dtype=int)
    for row, cname in enumerate(clipnames):
        m = rep.match(cname)
        print m.group(0)    # full filename
        if m.groups():
            year, magno, pageno, clipno = map(int, m.groups())
            cliparr[row, :] =  [year, magno, pageno, clipno]
    return cliparr

datadir = 'allclips2/'
hists, clipnames, clips, clipsizes = process_clipfiles(datadir)
hists = np.array(hists)
clipmeta = numpyfy_clipnames(clipnames)
clipmeta = np.hstack((clipmeta, np.array(clipsizes)[:, np.newaxis]))

svm = cv2.SVM()
svm.load('svm_final.yaml')

preds = svm.predict_all(hists)   # text ==0, image ==1
clipmeta = np.hstack((clipmeta, preds))

# save for later usage
np.save('clip_meta', clipmeta)
# save also as csv (can be analysed later with R, pandas, ...)
np.savetxt('clip_meta.csv', clipmeta, fmt='%d', delimiter=',',
        header='"year", "no", "page", "clipno", "area", "class"')

