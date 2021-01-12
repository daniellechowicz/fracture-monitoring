# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 09:40:09 2021

@author: Daniel Lechowicz
"""

import cv2
import numpy as np
import os
import sys

# Define static strings containing root and filename.
# Change these strings to indicate where the videos are.
ROOT = "F:\\02 Work\\07 Babu\\PRF\\Videos\\PRF0.1"
FILENAME = "PRF0.1-2.MP4"

path = os.path.join(ROOT, FILENAME)

# This static string determines the step (corresponding to the of the matrix's column).
# The lower the step, the more accurate results you get (1 corresponds to the most accurate results).
# However, the lower the step, the slower the analysis.
STEP = 1


class FramePreprocessing:
        
    def transformImage(self, frame):
        
        # Change to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        
        # Perform Otsu's thresholding after Gaussian filtering.
        kernel = (3, 3)
        blur = cv2.GaussianBlur(gray, kernel, 0)
        ret, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Apply mask.
        mask = cv2.bitwise_not(th)
        frame[:, :, 0] = frame[:, :, 0] * mask
        frame[:, :, 1] = frame[:, :, 1] * mask
        frame[:, :, 2] = frame[:, :, 2] * mask
        
        return frame, th
    
    def findCrack(self, x, w, y, h, frame, mask):
        
        # Loop column by column - only within coordinates obtained by means of "findContours" function.
        for i in range(x, x+w):
            
            # Step specified above (change to increase or decrease algorithm's accuracy/speed ratio).
            if i % STEP == 0:
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
                    
                    # Append to global variable (used for calculation of mean crack's width and crack's area).
                    widths.append(abs(start-stop))
                    area.append(abs(start-stop) * STEP)
                    
                    cv2.line(frame, (i, start), (i, stop), (0, 255, 0), 1)

                except:
                    # If no lines were present, stop the process.
                    # This means that the tip of the crack was found.
                    break
        
    def findContours(self, frame, mask):
        
        if (int(cv2.__version__[0]) > 3):
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        else:
            im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
        if len(contours) != 0:
            # Find the biggest countour (c) by the area.
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
    
            # Draw the biggest area only.
            cv2.drawContours(frame, c, -1, (0, 255, 255), 1)
    
            # Describe the largest contour with a rectangle.
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
        
        return x, y, w, h
            

def main():
    
    # Declare global variables where information regarding analysed crack will be saved.
    # These are global variables since it is easier to access them this way.
    global widths, area
    widths = []
    area = []
    
    # Create a "VideoCapture" object and read from input file.
    cap = cv2.VideoCapture(path)
    
    # Check if camera has been opened successfully.
    # Otherwise, exit the program.
    if (cap.isOpened()== False): 
        sys.exit("Error opening video stream or file")    
        
    # Get number of frames of the video (to calculate its duration later on).
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Read until video is completed...
    while(cap.isOpened()):    
        # Capture frame-by-frame.
        ret, frame = cap.read()
        
        if ret == True:
            # Find OpenCV version and get FPS of the video.
            (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
            if int(major_ver) < 3:
                fps = int(cap.get(cv2.cv.CV_CAP_PROP_FPS))
            else:
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                
            # Get video's properties (current timestamp, current_frame, its duration and progress done).
            timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            currentFrame = int((timestamp*fps)/1000)
            duration = frameCount/fps
            progress = int((timestamp*0.1)/duration)
            
            # Run second after second (otherwise, it would take too long).
            if currentFrame % fps == 0:
                # Initialize a "frameProcessing" object.
                framePreprocessing = FramePreprocessing()
                
                # Perform necessary transformations (scroll up to see the function).
                frame, mask = framePreprocessing.transformImage(frame)
                
                # Find contours.
                x, y, w, h = framePreprocessing.findContours(frame, mask)
                
                # Find crack.
                framePreprocessing.findCrack(x, w, y, h, frame, mask)
                
                # Add some information that user might find useful.
                # Declare static variables used to formate text label.
                FONT = cv2.FONT_HERSHEY_SIMPLEX        
                FONT_SCALE = 1
                FONT_COLOUR = (0, 0, 255)
                FONT_THICKNESS = 2
    
                label = "Timestamp: {} s\n".format(int(timestamp/1000)) + \
                        "Current frame: {} \n".format(currentFrame) + \
                        "Progress: {}% \n".format(progress) + \
                        "Crack mean width: {} px\n".format(round(np.mean(widths), 2)) + \
                        "Crack area: {} px squared".format(round(sum(area), 2))
                
                # Reset the vectors (as they need to be empty for each consecutive frame).
                widths = []
                area = []
    
                for i, line in enumerate(label.split('\n')):
                    # Get width and height of the label to calculate break between lines.
                    (labelWidth, labelHeight), baseline = cv2.getTextSize(label, FONT, FONT_SCALE, FONT_THICKNESS)
                    
                    # Increment function.
                    # X coordinate fixed (no multiplication by "i" variable).
                    # Y coordinate multiplied by 2 to add interline effect - no touch between consecutive lines.
                    x = 25
                    y = int(25 + labelHeight + i * labelHeight * 2)
                    
                    cv2.putText(frame, line, (x, y), FONT, FONT_SCALE, FONT_COLOUR, FONT_THICKNESS, cv2.LINE_AA) 
                    
                # Display the resulting frame.
                cv2.imshow('Frame', frame)
            
            # Press "Q" on keyboard to exit.
            if cv2.waitKey(25) & 0xFF == ord('q'):
              break
        
        # Break the loop.
        else: 
            break
    
    # When everything done, release the video capture object.
    cap.release()
    
    # Closes all the frames.
    cv2.destroyAllWindows()
    
    
if __name__ == "__main__":
    main()