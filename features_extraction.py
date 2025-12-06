import cv2
from flask import Flask, Response

app = Flask(__name__)

video = cv2.VideoCapture('./sample.mp4')
#  orb (oriented fast and rotated brief) -> finds corners and texture details
orb = cv2.ORB_create(nfeatures=5000) 

def make_frames():
    while True:
        ret, frame = video.read()

        # getting features 
        points, id= orb.detectAndCompute(frame, None)
        frame = cv2.drawKeypoints(frame, points, None, color=(0,255,0), flags=0)

        # encode frame into jpg 
        ok, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # no retunr
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def feed():
    return Response(make_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


    