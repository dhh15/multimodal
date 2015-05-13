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
        clip_image = cv2.imread(dirname + clip_name)
        hist3c = calc_hist(clip_image)
        hist_flat = hist3c.flatten()
        flathists.append(hist_flat)
        clipnames.append(clip_name)

    return flathists, clipnames

# get training data

text_dir = "text/"
image_dir = "images/"

text_hists = np.array(get_flathists(text_dir)[0])
image_hists = np.array(get_flathists(image_dir)[0])

# save copies with pickle
with open('texthists_dump', 'w') as tf:
    pickle.dump(text_hists, tf)

with open('imagehists_dump', 'w') as imf:
    pickle.dump(image_hists, imf)

train_hist_data = np.vstack((text_hists, image_hists))
text_responses = np.float32(np.repeat(0,len(text_hists))[:,np.newaxis])
image_responses = np.float32(np.repeat(1,len(image_hists))[:,np.newaxis])
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
svm.save('svm_test.yaml')

# compare with train_auto, which should do cross-validation automatically (assuming I'm calling it correctly)
svm_auto =cv2.SVM()
svm_auto_params  = dict( kernel_type = cv2.SVM_LINEAR,svm_type = cv2.SVM_C_SVC)
svm_auto.train_auto(train_hist_data, train_responses, None, None, params=svm_auto_params, k_fold=2)
svm_auto.save('svm_auto.yaml')

# get some testdata
test_dir = "testclips/"

test_hists, test_names = get_flathists(test_dir)
test_hists = np.array(test_hists)

# THE MAGIC
test_preds = svm.predict_all(test_hists)
test_preds_auto = svm_auto.predict_all(test_hists)

# let's look at results
for i, name in enumerate(test_names):
    print name, test_preds[i], test_preds_auto[i]
    # it works?!
