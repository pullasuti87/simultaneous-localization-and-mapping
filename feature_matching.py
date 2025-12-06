import cv2
# import numpy

video = cv2.VideoCapture("sample.mp4")
orb = cv2.ORB_create(nfeatures=1000)

# ?????? DO I NEEED THIS
"""
 bfmatcher = brute force matcher 
 ompares point in frame1 with point in frame2
 norm_hamming -> some math method that is needed, check it up
"""
# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

ret, frame1 = video.read()

# points need to be grey
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
# feature in frame1
point1, descr1 = orb.detectAndCompute(gray1, None)

# same with frame2
ret, frame2 = video.read()
gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
point2, descr2 = orb.detectAndCompute(gray2, None)


#print("frame1:", frame1)
print("frame2:", frame2)
video.release()
cv2.destroyAllWindows()
