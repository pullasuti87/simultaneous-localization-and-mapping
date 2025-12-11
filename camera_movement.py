import cv2
import numpy
import math

SCALE = 50.0
OFFSET = (300, 500)

video = cv2.VideoCapture("sample.mp4")

# draw path on canvas, trajectory Visualization 
def draw(img, v): # v -> vector (x, y, z)
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

    cv2.putText(traj, 'SLAM', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return traj

# while True:
#     ret, frame = video.read()
#     if not ret:
#         break
# 

print("test")

# init matrix
m = numpy.eye(4)

# counter 
i = 0

while True:
    # camera is moving up z and go left and right x
    test_z= -(i * 0.05) 
    # go left and right
    test_x= math.sin(i * 0.1) * 2.0 

    # andd numbers to matrix 
    m[0, 3] = test_x 
    m[2, 3] = test_z

    # blank canvas
    t = draw(None, m)

    cv2.imshow('', t)

    i += 1

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

