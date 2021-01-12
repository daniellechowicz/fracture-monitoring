# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 09:42:30 2021

@author: Daniel Lechowicz
"""

import cv2
import numpy as np
import os
from threading import Thread
from time import sleep

# Define static strings containing root and filename.
# Change these strings to indicate where the videos are.
ROOT = "F:\\02 Work\\07 Babu\\PRF\\Videos\\PRF0.1"
FILENAME1 = "testVideo1.mp4"
FILENAME2 = "testVideo2.mp4"


class PointTracker:
    
    def __init__(self, path, frameName):
        self.cap = cv2.VideoCapture(path)
        self.frameName = frameName
        
        # Lucas-Kanade method's parameters
        self.lk_params = dict(winSize = (15, 15),
                              maxLevel = 4,
                              criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        
        # Initial frames (needed for further processing)
        _, self.frame = self.cap.read()
        self.oldGray1 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.oldGray2 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.oldGray3 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.oldGray4 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        
        cv2.namedWindow(self.frameName)
        cv2.setMouseCallback(self.frameName, self.selectPoint)
        
        # Reset the points
        self.resetPoints()

        # Threading (in order to synchronize multiple videos)
        # self.thread = Thread(target=self.start, args=())
        # self.thread.daemon = True
        # self.thread.start()
        
    def resetPoints(self):
        # Based on this variable, dots will be marked
        # e.g. when counter is set to 0, the first dot will be marked
        self.counter = 0

        # Dot no. 1
        self.point1 = ()
        self.oldPoints1 = np.array([[]])
        # Dot no. 2
        self.point2 = ()
        self.oldPoints2 = np.array([[]])
        # Dot no. 3
        self.point3 = ()
        self.oldPoints3 = np.array([[]])
        # Dot no. 4
        self.point4 = ()
        self.oldPoints4 = np.array([[]])

    def selectPoint(self, event, x, y, flags, params):
        # global point, point_selected, old_points
        if event == cv2.EVENT_LBUTTONDOWN:
            # Update counter
            self.counter += 1

            if self.counter == 1:
                self.point1 = (x, y)
                self.oldPoints1 = np.array([[x, y]], dtype=np.float32)
            elif self.counter == 2:
                self.point2 = (x, y)
                self.oldPoints2 = np.array([[x, y]], dtype=np.float32)
            elif self.counter == 3:
                self.point3 = (x, y)
                self.oldPoints3 = np.array([[x, y]], dtype=np.float32)
            elif self.counter == 4:
                self.point4 = (x, y)
                self.oldPoints4 = np.array([[x, y]], dtype=np.float32)
            else:
                self.resetPoints()

    def drawPoint(self, number, frame, grayFrame):
        colours = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "orange": (255, 215, 0)} 
        circleDiameter = -1
        lineLength = 5
        thickness = 1

        if number == 1:
            newPoints, status, error = cv2.calcOpticalFlowPyrLK(self.oldGray1, grayFrame, self.oldPoints1, None, **self.lk_params)
            self.oldGray1 = grayFrame.copy()
            self.oldPoints1 = newPoints
    
            x, y = newPoints.ravel()
            cv2.circle(frame, (x, y), 1, colours["red"], circleDiameter)
            cv2.line(frame, (int(x-lineLength), int(y)), (int(x+lineLength), int(y)), colours["red"], thickness)
            cv2.line(frame, (int(x), int(y-lineLength)), (int(x), int(y+lineLength)), colours["red"], thickness)
        
        if number == 2:
            newPoints, status, error = cv2.calcOpticalFlowPyrLK(self.oldGray2, grayFrame, self.oldPoints2, None, **self.lk_params)
            self.oldGray2 = grayFrame.copy()
            self.oldPoints2 = newPoints
    
            x, y = newPoints.ravel()
            cv2.circle(frame, (x, y), 1, colours["green"], circleDiameter)
            cv2.line(frame, (int(x-lineLength), int(y)), (int(x+lineLength), int(y)), colours["green"], thickness)
            cv2.line(frame, (int(x), int(y-lineLength)), (int(x), int(y+lineLength)), colours["green"], thickness)

        if number == 3:
            newPoints, status, error = cv2.calcOpticalFlowPyrLK(self.oldGray3, grayFrame, self.oldPoints3, None, **self.lk_params)
            self.oldGray3 = grayFrame.copy()
            self.oldPoints3 = newPoints
    
            x, y = newPoints.ravel()
            cv2.circle(frame, (x, y), 1, colours["blue"], circleDiameter)
            cv2.line(frame, (int(x-lineLength), int(y)), (int(x+lineLength), int(y)), colours["blue"], thickness)
            cv2.line(frame, (int(x), int(y-lineLength)), (int(x), int(y+lineLength)), colours["blue"], thickness)

        if number == 4:
            newPoints, status, error = cv2.calcOpticalFlowPyrLK(self.oldGray4, grayFrame, self.oldPoints4, None, **self.lk_params)
            self.oldGray4 = grayFrame.copy()
            self.oldPoints4 = newPoints
    
            x, y = newPoints.ravel()
            cv2.circle(frame, (x, y), 1, colours["orange"], circleDiameter)
            cv2.line(frame, (int(x-lineLength), int(y)), (int(x+lineLength), int(y)), colours["orange"], thickness)
            cv2.line(frame, (int(x), int(y-lineLength)), (int(x), int(y+lineLength)), colours["orange"], thickness)

    def start(self):
        while True:
            _, frame = self.cap.read()
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Iterate through the points (based on the counter value)
            for i in range(0, self.counter):
                self.drawPoint(i+1, frame, grayFrame)

            cv2.imshow(self.frameName, frame)
            sleep(0.1)
            key = cv2.waitKey(1)
            if key == 27:
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    path1 = os.path.join(ROOT, FILENAME1)
    path2 = os.path.join(ROOT, FILENAME2)

    pt1 = PointTracker(path1, "f1").start()
    # pt2 = PointTracker(path2, "f2")