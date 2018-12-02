import cv2
import numpy as np
img = cv2.imread('lunkuo.png')

ret,thresh = cv2.threshold(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),127,255,0) 
cv2.imshow('lunkuo',thresh)
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cnt = contours[0]
M = cv2.moments(cnt)

imgnew = cv2.drawContours(img, contours, -1, (0,255,0), 3)#????????
print (M['m00'])
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

area = cv2.contourArea(cnt)

perimeter = cv2.arcLength(cnt,True)

epsilon = 0.02*perimeter
approx = cv2.approxPolyDP(cnt,epsilon,True)
imgnew1 = cv2.drawContours(img, approx, -1, (0,0,255), 3)

cv2.imshow('lunkuo',imgnew)
cv2.imshow('approx_lunkuo',imgnew1)