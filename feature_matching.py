import cv2
# import numpy 

video = cv2.VideoCapture('sample.mp4')

orb = cv2.ORB_create(nfeatures=1000)

"""
 bfmatcher = brute force matcher 
 ompares point in frame1 with point in frame2
 norm_hamming -> some math method that is needed, check it up
"""
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

ret, old_frame = video.read()

video.release()
cv2.destroyAllWindows()