import cv2
import numpy as np
import copy

src = cv2.imread('../sheetmusic/sample.jpg', 0) #this 0 means load greyscale

grey = src #this is a place holder because we fixed laoding it in greyscale in imread
bw = cv2.adaptiveThreshold(~grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2);

horizontal = copy.deepcopy(bw)
vertical = copy.deepcopy(bw)
attempt = copy.deepcopy(bw)

print len(horizontal)
print len(horizontal[0])

horizontalsize = len(horizontal[0]) // 30
horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize, 1))
horizontal = cv2.erode(horizontal, horizontalStructure, (-1, -1))
horizontal =cv2.dilate(horizontal, horizontalStructure, (-1, -1));

verticalsize = len(vertical[0]) // 30
verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
vertical = cv2.erode(vertical, verticalStructure, (-1, -1))
vertical =cv2.dilate(vertical, verticalStructure, (-1, -1));

attemptsize = 3
attemptStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, attemptsize))
attempt = cv2.erode(attempt, attemptStructure, (-1, -1))
attempt = cv2.dilate(attempt, attemptStructure, (-1, -1));
attempt = ~attempt #to get the notes black again
detector = cv2.SimpleBlobDetector_create()
keypoints = detector.detect(attempt)
attempt_with_keypoints = cv2.drawKeypoints(attempt, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

#shows the end resutls verticallyc concatinated
#cv2.imshow('grey', grey)
#cv2.imshow('bw', bw)
#cv2.imshow('horizontal', ~horizontal)
#cv2.imshow('vertical', ~vertical)
#cv2.imshow('attempt', ~attempt)
imageToShow = np.concatenate((grey, ~horizontal, ~vertical, attempt), axis = 0)
cv2.imshow('progression', imageToShow)
cv2.imshow('withkp', attempt_with_keypoints)
while True:
    k = cv2.waitKey(0)
    print k
    if k == 27 or k == 1048603:
        break

cv2.destroyAllWindows()

