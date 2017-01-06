import cv2
import numpy as np
import copy


#create parameters

#src = cv2.imread('../sheetmusic/sample.jpg', 0) #this 0 means load greyscale

src = cv2.imread('../sheetmusic/ode-to-joy-sheet-music.jpg', 0) #this 0 means load greyscale
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

attemptsize = 2
attemptStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, attemptsize))
attempt = cv2.erode(attempt, attemptStructure, (-1, -1))
attempt = cv2.dilate(attempt, attemptStructure, (-1, -1));
attempt = ~attempt #to get the notes black again

blurredattempt = cv2.blur(attempt, (3, 3))
cv2.imshow('blur attempt', blurredattempt)

dark_blobs = True
min_area = 1
def resetParams():
    params = cv2.SimpleBlobDetector_Params()
    params.filterByColor = 1
    params.blobColor = (0 if dark_blobs else 255)
    params.minThreshold = 10
    params.maxThreshold = 220
    params.filterByArea = True
    params.minArea = min_area
    params.filterByCircularity = True
    params.minCircularity = 0.75
    params.maxCircularity = 1
    params.filterByConvexity = False
    params.filterByInertia = False
    detector = cv2.SimpleBlobDetector_create(params)
    '''
    params = cv2.SimpleBlobDetector_Params()
    # Change thresholds
    params.minThreshold = 1
    params.maxThreshold = 2000

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 1
#    params.maxArea = float(raw_input('max area'))

    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0

    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0

    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.01

    #Set to look for black blobs
    params.blobColor = 0
    '''
    '''
    # Change thresholds
    params.minThreshold = float(raw_input('min thresholds'));
    params.maxThreshold = float(raw_input('max thresholds'));

    # Filter by Area.
    params.filterByArea = True
    params.minArea = float(raw_input('min area'))
#    params.maxArea = float(raw_input('max area'))

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = float(raw_input('min circularity'))

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = float(raw_input('min convexity'))

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = float(raw_input('min InertiaRatio'))
    '''
    #create blobdetector
    detector = cv2.SimpleBlobDetector_create(params)
    return detector


while True:
    k = cv2.waitKey(0)
    print k
    if k == 27 or k == 1048603:
        break
    detector = resetParams()
    keypoints = detector.detect(blurredattempt)
    attempt_with_keypoints = cv2.drawKeypoints(blurredattempt, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('withkp', attempt_with_keypoints)
    cv2.waitKey() #only here so it shows images
    '''
    #shows the end resutls verticallyc concatinated if small enough
    toLarge = True
    if toLarge == True:
        cv2.imshow('grey', grey)
        cv2.imshow('bw', bw)
        cv2.imshow('horizontal', ~horizontal)
        cv2.imshow('vertical', ~vertical)
        cv2.imshow('attempt', attempt)
        cv2.imshow('withkp', attempt_with_keypoints)
    else:
        imageToShow = np.concatenate((grey, ~horizontal, ~vertical, attempt), axis = 0)
        cv2.imshow('progression', imageToShow)
        cv2.imshow('withkp', attempt_with_keypoints)
    '''
cv2.destroyAllWindows()

