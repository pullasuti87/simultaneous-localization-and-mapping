import cv2
import numpy
import math

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

# default value given by ai 
focal = 1.0 * w
print(focal)
cp = (w / 2, h / 2)  # center point
print(cp)
# matrix for camera placeholder
ph = numpy.array([
    [focal, 0, cp[0]],
    [0, focal, cp[1]],
    [0, 0, 1]
], dtype=numpy.float32)

print(ph)

# while True:
#     ret, frame = video.read()
#     if not ret:
#         break
#
# print("test")
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
