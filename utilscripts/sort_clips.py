import cv2
import os
import shutil

images = os.listdir('00_trainclips')

for i in images:
    filename = "00_trainclips/" + str(i) # filename must include dir + filename
    if 'png' in filename:
        image = cv2.imread(filename) # read the image
        cv2.imshow("Image", image) # show the image
        keystroke = cv2.waitKey(0) # wait until a key is pressed
        if keystroke == ord('t'):
            shutil.copyfile(filename, './00_trainclips/00_texts/' + i)
        if keystroke == ord('i'):
            shutil.copyfile(filename, './00_trainclips/00_images/' + i)
        if keystroke == ord('x'):
            shutil.copyfile(filename, './00_trainclips/00_remove/' + i)
        else:
            continue

