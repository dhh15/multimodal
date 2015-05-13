# encoding: utf-8

# script: classify text / image clippings with historgram info

import numpy as np
import cv2

# helper function:

def calc_hist(clip):
    return cv2.calcHist([clip], [0,1,2], None, [8,8,8], [0, 256, 0,256, 0,256])


def get_flathists(dirname):
    dirlist = os.listdir(dirname)
    flathists = []
    for clip in dirlist:
        clip = cv2.imread(dirname + tclip)
        hist3c = calc_hist(clip)
        hist_flat = hist3c.flatten()
        flathists.append(hist_flat)

    return flathists

# get training data

text_dir = "folder/"
image_dir = "another_folder/"

text_hists = np.array(get_flathists(text_dir))
image_hists = np.array(get_flathists(image_dir))

# save copies with pickle
with open('texthists_dump', 'w') as tf:
    pickle.dump(text_hists, tf)

with open('imagehists_dump', 'w') as imf:
    pickle.dump(image_hists, imf)



