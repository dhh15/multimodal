# encoding: utf-8

# script: classify text / image clippings with historgram info
import os
import numpy as np
import cv2
import pickle

# helper function:

def calc_hist(clip):
    return cv2.calcHist([clip], [0,1,2], None, [8,8,8], [0, 256, 0,256, 0,256])


def get_flathists(dirname):
    dirlist = os.listdir(dirname)
    flathists = []
    clipnames = []
    for clip_name in dirlist:
        print clip_name
        clip_image = cv2.imread(dirname + clip_name)
        print clip_image.shape
        hist3c = calc_hist(clip_image)
        hist_flat = hist3c.flatten()
        flathists.append(hist_flat)
        clipnames.append(clip_name)

    return flathists, clipnames

# get training data

text_dir = "clips-217-texts/"
TEXT_C = 0
image_dir = "clips-89-images/"
IMAGE_C = 1

text_hists = np.array(get_flathists(text_dir)[0])
image_hists = np.array(get_flathists(image_dir)[0])

# save copies with pickle
with open('texthists_dump', 'w') as tf:
    pickle.dump(text_hists, tf)

with open('imagehists_dump', 'w') as imf:
    pickle.dump(image_hists, imf)

train_hist_data = np.vstack((text_hists, image_hists))
text_responses = np.float32(np.repeat(TEXT_C,len(text_hists))[:,np.newaxis])
image_responses = np.float32(np.repeat(IMAGE_C,len(image_hists))[:,np.newaxis])
train_responses = np.vstack((text_responses, image_responses))

svm = cv2.SVM()
svm_params = dict(  kernel_type = cv2.SVM_LINEAR,
                    # according to docs, linear kernel is the fastest; some tutorials recommend RBF
                    svm_type = cv2.SVM_C_SVC,       # use C-SVM (standard)
                    C=20.0,   # penalty term
                    gamma=5.0 )

# C, gamma are random guesses
# probs should e.g. divide training data into to 2 sets and cross-validate
svm.train(train_hist_data, train_responses, params=svm_params)

# alternatively use train_auto, which should do cross-validation automatically (assuming I'm calling it correctly)
# according to yaml dump, C is always 1.0?!
svm_auto =cv2.SVM()
svm_auto_params  = dict( kernel_type = cv2.SVM_LINEAR,svm_type = cv2.SVM_C_SVC)
svm_auto.train_auto(train_hist_data, train_responses, None, None, params=svm_auto_params, k_fold=2)
svm_auto.save('svm_auto.yaml')

## Test prediction accuracy:

test_text_dir = "clips-217-texts-2/"
test_image_dir = "clips-89-images-2/"

# get histograms for testtexts
test_texthists, _ = get_flathists(test_text_dir)
test_texthists = np.array(test_texthists)

# same for images
test_imagehists, _ = get_flathists(test_image_dir)
test_imagehists = np.array(test_imagehists)

# THE MAGIC
text_test_preds = svm.predict_all(test_texthists)
image_test_preds = svm.predict_all(test_imagehists)

# remember TEXT_C == 0, IMAGE_C = 1, so we can simply sum things up
nttext = len(text_test_preds)
ntimag = len(image_test_preds)
ncorrect_text = nttext - sum(text_test_preds)
ncorrect_image = sum(image_test_preds)
print "text recog accuracy", 1.0*ncorrect_text/nttext
print "image recog accuracy", 1.0*ncorrect_image/ntimag
print "total accuracy", (1.0*ncorrect_text +ncorrect_image)/(nttext + ntimag)

# objective: find such values for kernel type, C and nu  that we reach acceptable recognition accuracy
# this could be automated, but we can get good enough results with just trying something

# when done (= we have good svm), save it:
svm.save("svm_final.yaml")    # we can load this in another script to do the large scale classifying
