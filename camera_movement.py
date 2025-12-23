import cv2
import numpy
# import math

"""https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html"""

SCALE = 50.0
OFFSET = (300, 500)

video = cv2.VideoCapture("sample.mp4")
orb = cv2.ORB_create(nfeatures=1000)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

# draw path on canvas, trajectory Visualization


def draw(img, v):  # v -> vector (x, y, z)
    global SCALE, OFFSET
    # blank canvas size
    traj = numpy.zeros((600, 600, 3), dtype=numpy.uint8)

    # extract x and z
    x = int(v[0, 3] * SCALE) + OFFSET[0]
    z = int(v[2, 3] * SCALE) + OFFSET[1]

    # camera position
    cv2.circle(traj, (x, z), 3, (0, 255, 0), -1)

    # draw line
    cv2.line(traj, OFFSET, (x, z), (255, 0, 0), 1)

    return traj


# frame dimensions from camera matrix
w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))


""" ????? is this needed..."""
# based by width
# focal = 1.0 * w
# print(focal)
# cp = [w / 2, h / 2]  # center point
# print(cp)
# # matrix for 3D coordinates to 2D pixels
# K = numpy.array([
#     [focal, 0, cp[0]],
#     [0, focal, cp[1]],
#     [0, 0, 1]
# ], dtype=numpy.float32)
#
# print(K)

        
# creates 4x4 matrix, where camera is now
v = numpy.eye(4)
# print(v)

ret, frame1 = video.read()
if not ret:
    print("fail frame1")
    exit()

gray_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

point1, description1 = orb.detectAndCompute(gray_frame1, None)


while True:
    ret, frame2 = video.read()
    if not ret:
        # print("frame2 fail")
        break

    gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    point2, description2 = orb.detectAndCompute(gray_frame2, None)

    if description1 is None or description2 is None:
        print("no descriptions")
    else:
        matches = bf.knnMatch(description1, description2, k=2)
        t = [] # GOOD matches
        for j, i in matches:
            if j.distance < 0.75 * i.distance:
                    t.append(j)
        # print(t)

    # old and new point
    fr1 = []
    fr2 = []

    for i in t:
        fr1.append(point1[i.queryIdx].pt)
    pt1 = numpy.float32(fr1).reshape(-1, 1 ,2)

    for j in t:
        fr2.append(point2[j.trainIdx].pt)
    pt2 = numpy.float32(fr2).reshape(-1, 1 ,2)
    
    
    print(pt1)
    print(pt2)

gray_frame1 = gray_frame2
point1 = point2
description1 = description2
#
# init matrix
# m = numpy.eye(4)
#
# counter
# i = 0
#
# while True:
#    # camera is moving up
#    z = -(i * 0.05)
#    print(z)
#    # go left and right
#    x = math.sin(i * 0.1) * 5.0
#    print(x)
#    # andd numbers to matrix
#    m[0, 3] = x
#    m[2, 3] = z
#
#    # blank canvas
#    t = draw(None, m)
#    cv2.imshow('', t)
#    i += 1
#
#    if cv2.waitKey(30) & 0xFF == ord('q'):
#        break
#
video.release()
cv2.destroyAllWindows()
