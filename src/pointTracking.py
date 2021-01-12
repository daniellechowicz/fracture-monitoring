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
        self.oldGray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        
        cv2.namedWindow(self.frameName)
        cv2.setMouseCallback(self.frameName, self.selectPoint)
        
        # These variables will be changed whenever click event is present
        self.point = ()
        self.pointSelected = False
        self.oldPoints = np.array([[]])
        
        # Threading (in order to synchronize multiple videos)
        self.thread = Thread(target=self.start, args=())
        self.thread.daemon = True
        self.thread.start()
        
    def selectPoint(self, event, x, y, flags, params):
        # global point, point_selected, old_points
        if event == cv2.EVENT_LBUTTONDOWN:
            self.point = (x, y)
            self.pointSelected = True
            self.oldPoints = np.array([[x, y]], dtype=np.float32)
      
    def start(self):
        while True:
            _, frame = self.cap.read()
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
            if self.pointSelected is True:
                cv2.circle(frame, self.point, 5, (0, 0, 255), 2)
        
                newPoints, status, error = cv2.calcOpticalFlowPyrLK(self.oldGray, grayFrame, self.oldPoints, None, **self.lk_params)
                self.oldGray = grayFrame.copy()
                self.oldPoints = newPoints
        
                x, y = newPoints.ravel()
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        
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

    pt1 = PointTracker(path1, "f1")
    pt2 = PointTracker(path2, "f2")