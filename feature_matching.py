import cv2

video = cv2.VideoCapture("sample.mp4")
orb = cv2.ORB_create(nfeatures=1000)

"""
 bfmatcher = brute force matcher 
 compares point in frame1 with point in frame2
 norm_hamming -> some math method that is needed, check it up
"""
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

ret, frame1 = video.read()

# points need to be grey
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
# feature in frame1
point1, descr1 = orb.detectAndCompute(gray1, None)

while True:
    ret, frame2 = video.read()
    if not ret:
        break

    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    point2, descr2 = orb.detectAndCompute(gray2, None)

    # check first and second best in descr2 to desrc1
    matches = bf.knnMatch(descr1, descr2, k=2)
    t = []
    for m, n in matches:
        # print(m.queryIdx,m,n)
        # only keep matches where the best is much better than the second
        if m.distance < 0.75 * n.distance:
            t.append(m)
    # print(t)

    # draw line between points
    f_matching = cv2.drawMatches(
        frame1,
        point1,
        frame2,
        point2,
        t,
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )
    print(f_matching)
    cv2.imshow("SLAM matching test", f_matching)

    frame1 = frame2.copy()
    point1 = point2
    descr1 = descr2

    # needed for video to play
    cv2.waitKey(1)

# print("frame1:", frame1)
# print("frame2:", frame2)
video.release()
cv2.destroyAllWindows()
