
# app.py
# based on tutorial ==> https://blog.miguelgrinberg.com/post/video-streaming-with-flask


from flask import Flask, render_template, Response
from camera_pi import Camera


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/video_feed.html')
def feed():
    """Video streaming home page."""
    return render_template('video_feed.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':  
    
    ssl_context = ('cert.pem','key.pem')
    app.run(host='0.0.0.0',ssl_context= ssl_context, debug=True, threaded=True)
