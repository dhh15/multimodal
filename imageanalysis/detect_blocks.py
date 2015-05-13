
# coding: utf-8

# Import necessary packages.

# In[34]:

import cv2
import mahotas


# Load image.

# In[35]:

image = cv2.imread('bluewings.png')


# Convert image to grayscale.

# In[36]:

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# Apply bilinear blurring.

# In[37]:

blurred = cv2.bilateralFilter(gray, 9, 21, 21)


# Calculate threshold using Otsu's method.

# In[38]:

T = mahotas.thresholding.otsu(blurred)


# Threshold image.

# In[39]:

_, thresh = cv2.threshold(blurred, T, 255, cv2.THRESH_BINARY_INV)


# Dilate image.
# 
# <blockquote>
# Note that the values for the kernel and iterations must be adjusted according to the data. If the data contains very little negative space and the content is packed together, the values must be lowered for detecting their boundaries.
# </blockquote>

# In[40]:

kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
dilated = cv2.dilate(thresh, kernel, iterations = 4)


# Close gaps in the image.

# In[41]:

closing = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, closing, iterations = 5)


# In[42]:

cv2.imwrite("01_closed.png", closed)


# Find contours.
# <blockquote>
# How about removing small elements <b>not</b> positioned close to margin using <i>x</i> and <i>y</i> values?
# </blockquote>

# In[43]:

contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
for contour in contours:
    [x, y, w, h] = cv2.boundingRect(contour)
    if h <= 0.02*image.shape[0] or w <= 0.02*image.shape[1]:
        continue
    cv2.rectangle(image, (x, y), (x+w, y+h), (171, 149, 39), 2)


# Write image on disk.

# In[44]:

cv2.imwrite("02_contours.png", image)


# In[ ]:



