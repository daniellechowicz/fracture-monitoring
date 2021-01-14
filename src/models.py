# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

class Video:

    def __init__(self, path, frameName):
        self.path = path
        self.frameName = frameName
        self.setup()

    def setup(self):
        # Open video capture
        self.open()

        # Lucas-Kanade method's parameters
        self.lk_params = dict(winSize = (15, 15),
                              maxLevel = 4,
                              criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    
        self.oldGray1 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.oldGray2 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.oldGray3 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.oldGray4 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        
        cv2.namedWindow(self.frameName)
        cv2.setMouseCallback(self.frameName, self.selectPoint)
        
        # Reset the points
        self.resetPoints()

    def open(self):
        self.cap = cv2.VideoCapture(self.path)
        # Initial frames (needed for further processing)
        _, self.frame = self.cap.read()

    def getPoints(self):
        if self.point1 == () and self.point2 == () and self.point3 == () and self.point4 == ():
            return None
        else:
            return self.point1, self.point2, self.point3, self.point4

    def getOldPoints(self):
        return self.oldPoints1, self.oldPoints2, self.oldPoints3, self.oldPoints4

    def setPoints(self, p1, p2, p3, p4):
        self.point1 = p1
        self.point2 = p2
        self.point3 = p3
        self.point4 = p4

        self.oldPoints1 = np.array([[p1[0], p1[1]]], dtype=np.float32)
        self.oldPoints2 = np.array([[p2[0], p2[1]]], dtype=np.float32)
        self.oldPoints3 = np.array([[p3[0], p3[1]]], dtype=np.float32)
        self.oldPoints4 = np.array([[p4[0], p4[1]]], dtype=np.float32)

        self.oldGray1 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.oldGray2 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.oldGray3 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.oldGray4 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        
    def resetPoints(self):
        self.counter = 0
    
        # Point no. 1
        self.point1 = ()
        self.oldPoints1 = np.array([[]])
        # Point no. 2
        self.point2 = ()
        self.oldPoints2 = np.array([[]])
        # Point no. 3
        self.point3 = ()
        self.oldPoints3 = np.array([[]])
        # Point no. 4
        self.point4 = ()
        self.oldPoints4 = np.array([[]])

    def selectPoint(self, event, x, y, flags, params):
        if self.point1 != () and self.point2 != () and self.point3 != () and self.point4 != ():
            p1, p2, p3, p4 = self.getPoints()
            self.oldPoints1 = np.array([[p1[0], p1[1]]], dtype=np.float32)
            self.oldPoints2 = np.array([[p2[0], p2[1]]], dtype=np.float32)
            self.oldPoints3 = np.array([[p3[0], p3[1]]], dtype=np.float32)
            self.oldPoints4 = np.array([[p4[0], p4[1]]], dtype=np.float32)
            
        if event == cv2.EVENT_LBUTTONDOWN:
            # Update counter
            self.counter += 1

            # Update another counter used for frame only
            self.getFrameCounter += 1

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

    def markPoints(self):
        _, frame = self.cap.read()
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Initialize the "getFrameCounter" ("counter" is reset, so it was necessary to create a counter that is incremental
        # in order to count the number of points marked and block the drawing function when the "getFrameCounter" exceeds 4)
        self.getFrameCounter = 0
        while True:
            if self.getFrameCounter < 4:
                self.drawPoint(self.getFrameCounter, frame, grayFrame)
                cv2.imshow(self.frameName, frame)
                if cv2.waitKey(20) & 0xFF == 27:
                    break
            else:
                break   
        cv2.destroyAllWindows()

        if self.getPoints() == None:
            pass
        else:
            p1, p2, p3, p4 = self.getPoints()
            self.setPoints(p1, p2, p3, p4)

    def getFrameTimestamp(self):
        # Number of frames of the video
        frameCount = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)

        # Find OpenCV version and get the FPS value of the video.
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        if int(major_ver) < 3:
            fps = self.cap.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            
        # Get:
        # - current timestamp, 
        # - current frame, 
        # - video's duration,
        # - progress done,
        # respectively.
        ts = self.cap.get(cv2.CAP_PROP_POS_MSEC)/1000 # [s]
        currentFrame = ts*fps/1000
        duration = frameCount/fps
        progress = ts*0.1/duration

        return ts, fps
        
    def getFrame(self, timestamp=False):
        ret, frame = self.cap.read()
        if ret:
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Iterate through the points (based on the counter value)
            for i in range(0, self.counter):
                self.drawPoint(i+1, frame, grayFrame)

            if timestamp:
                ts, fps = self.getFrameTimestamp()
            else:
                ts, fps = None, None

        return ret, frame, ts, fps

class CrackLength:

    def __init__(self, path):
        # Video path
        self.path = path

        # Workpiece dimensions [mm]
        self.length = 200
        self.incisionLength = 30
        
        # Instead of global variables
        self.widths = []
        self.area = []
        
        # Open video capture
        self.open()

    def open(self):
        self.cap = cv2.VideoCapture(self.path)

    def transformImage(self, frame):
        # Change to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        
        # Perform Otsu's thresholding after Gaussian filtering
        kernel = (3, 3)
        blur = cv2.GaussianBlur(gray, kernel, 0)
        _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return frame, th

    def getCrackLength(self, crackTip, leftEdge, rightEdge):
        length = rightEdge - leftEdge
        incisionLength = length * (self.incisionLength/self.length)
        crackLength = length - incisionLength - (rightEdge-crackTip)
        
        # Convert to [mm]
        crackLength = (crackLength/length) * self.length

        return crackLength

    def findCrack(self, x, w, y, h, frame, mask):        
        # Loop column by column, but only within coordinates 
        # obtained by means of "findContours" function
        for i in range(x, x+w):
            container = []
            indices = []
            scores = []
            
            # The task of the following lines is to scan the column row by row 
            # and then add 1 to the vector "container" when the value of an individual pixel 
            # is equal to "0" (which corresponds to white). Otherwise, the "container" is reset. 
            # The motivation behind this idea was to find the longest possible sequence of white color, 
            # which in most of the cases indicates searched crack.
            for j in range(int(y+0.25*h), int(y+h-0.25*h)):
                if mask[j, i] == 0:
                    container.append(1)
                    score = sum(container)
                    scores.append(score)
                    indices.append(j)
                else:
                    container = []
    
            try:
                where = scores.index(max(scores))
                start = indices[where] - scores[where]
                stop = indices[where]

                # Draw lines (crack)    
                cv2.line(frame, (i, start), (i, stop), (0, 255, 0), 1)
                
            except:
                # If no lines were present, stop the process
                # This means that the tip of the crack was found
                break
                    
        return self.getCrackLength(i, x, x+w)
        
    def findContours(self, frame, mask):
        if (int(cv2.__version__[0]) > 3):
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        else:
            im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
        if len(contours) != 0:
            # Find the biggest countour (c) by the area
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
    
            # Draw the biggest area only
            cv2.drawContours(frame, c, -1, (0, 255, 255), 1)
    
            # Describe the largest contour with a rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
        
        return x, y, w, h

    def getFrame(self):
        ret, frame = self.cap.read()

        # Perform necessary transformations (scroll up to see the function)
        frame, mask = self.transformImage(frame)
        
        # Find contours
        x, y, w, h = self.findContours(frame, mask)

        # Find crack and get its value
        crackLength = self.findCrack(x, w, y, h, frame, mask)
        
        return ret, frame, crackLength

class Data:

    def __init__(self, path):
        self.path = path

    def upload(self):
        data = np.loadtxt(self.path, delimiter=";")
        travel = data[:, 0]
        force = data[:, 1]
        t = data[:, 2]

        return travel, force, t

    def preview(self, previewTravel=False, previewForce=False):
        travel, force, t = self.upload()
        
        plt.close("all")

        if previewTravel:
            plt.figure()
            plt.plot(t, travel, linewidth=0.5, linestyle="--", color="blue")
            plt.xlabel("Time [s]", fontsize=12)
            plt.ylabel("Standard travel [mm]", fontsize=12)

        if previewForce:
            plt.figure()
            plt.plot(t, force, linewidth=0.5, linestyle="--", color="blue")
            plt.xlabel("Time [s]", fontsize=12)
            plt.ylabel("Standard force [N]", fontsize=12)

        plt.show()