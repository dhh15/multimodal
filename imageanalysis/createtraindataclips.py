#!/usr/bin/env python
# encoding: utf-8

import numpy as np
import cv2
import os
import pickle

# our custo detecting tools
import bdetect

page_folder = "./trainpngs/" # one-page or double-page spread pngs
clip_folder = "./trainclips/"

# let's make them into clippings

pagedata = os.listdir(page_folder)

for imfile in pagedata:
    print page_folder + imfile
    image = cv2.imread(page_folder + imfile)
    im_boxes, contours, bound_rects = bdetect.detect_blocks(image.copy())
    clips = bdetect.produce_clips(bound_rects, image)
    for clipno, clip_image in enumerate(clips):
        cv2.imwrite(clip_folder + imfile +  "-clip-" + str(clipno) + ".png",clip_image)

