import cv2
import depthai as dai
import numpy as np

def getFrame(queue):
    #Get frame from the queue
    frame = queue.get()
    #convert the frmae to OpenCV format and return
    return frame.getCvFrame()

def getMonoCamera(pipeline, isLeft):
    #configure mono camera
    mono = pipeline.createMonoCamera()

 #set the Camera Resolution
    mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    if isLeft:
        mono.setBoardSocket(dai.CameraBoardSocket.LEFT)
    else:
        mono.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    return mono

if __name__ == '__main__':

    #define a pipeline
    pipeline = dai.Pipeline()

    #set up left and right cameras
    monoLeft = getMonoCamera(pipeline, isLeft = True)
    monoRight = getMonoCamera(pipeline, isLeft = False)

    #set output Xlink for left camera
    xoutLeft = pipeline.createXLinkOut()
    xoutLeft.setStreamName("left")

    #set output Xlink for right camera
    xoutRight = pipeline.createXLinkOut()
    xoutRight.setStreamName("right")

    #Attach cameras to output XLink 
    monoLeft.out.link(xoutLeft.input)
    monoRight.out.link(xoutRight.input)

    #pipeline is defined, now we can connect to the device
    with dai.Device(pipeline) as device:

        #get the output queues.
        leftQueue = device.getOutputQueue(name = 'left', maxSize=1)
        rightQueue = device.getOutputQueue(name = 'right', maxSize = 1)
        count=0
        while True:
            #get left Frame
            leftFrame = getFrame(leftQueue)
            #get right frame
            rightFrame = getFrame(rightQueue)

            cv2.imshow('left', leftFrame)
            cv2.imshow('right', rightFrame)

            #check for keyboard input
            key = cv2.waitKey(1)
            if key == ord('q'):
                break # quit when q is pressed
            elif key == ord('p'):
                cv2.imwrite(f'picture_left_{count}.png', leftFrame)
                cv2.imwrite(f'picture_right_{count}.png', rightFrame)
                count += 1