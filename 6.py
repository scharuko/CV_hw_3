# importing libraries
import cv2
import cv2.aruco as aruco
import numpy as np
import os
import  depthai as dai
# find the aruco marker in the image
def findArucoMarkers(img, markerSize =4, totalMarkers=50, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    # get the bounding box of the aruco markers
    bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    return (bboxs)
# load the camera images captured seperated by 7.5 cm
img0 = cv2.imread(r"C:\Users\sheet\OneDrive\Documents\ComputerVision\Assignement3\picture_left_1.png")
img1 = cv2.imread(r"C:\Users\sheet\OneDrive\Documents\ComputerVision\Assignement3\picture_right_1.png")

#disparity equation d = basline(8cm) * focallength(1.636331765375964e+03)/(ul - ur)

baseline = 7.5
focal_length = 1.636331765375964e+03

actual_measurement = 208.28000000000003

#we use the right corners of aruco markers
bbox1= findArucoMarkers(img0)
bbox2 = findArucoMarkers(img1)

print(bbox1[0][0][3][0])
print(bbox2[0][0][3][0])

d = (baseline * focal_length)/(bbox1[0][0][3][0]-bbox2[0][0][3][0])
print(f'Distance measured is {d} cm')
print(f'Actual distance is {actual_measurement} cm')
print(f'Error is {abs(d-actual_measurement)} cm')
# Distance measured is 208.28000000000003 cm
# Distance from disparity equation is 208.008 cm
# Error = 0.272 cm