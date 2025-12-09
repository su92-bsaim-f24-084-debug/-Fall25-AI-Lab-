from flask import Flask, render_template_string, Response, request, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import threading
import time

app = Flask(__name__)

# --------------------------- Configuration ---------------------------
MODEL_PATH = "emotion_detection_model.h5"  # path to your trained model
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
# Put your camera/source URL here (can be 0 for local webcam)
CAMERA_SOURCE = 0
# ---------------------------------------------------------------------

# Load model once (global)
model = load_model(MODEL_PATH)

# Haar cascade for face detection (OpenCV builtin)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# A thread-safe camera reader to continuously grab frames from the source
class CameraGrabber:
    def __init__(self, src=0):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.lock = threading.Lock()
        self.frame = None
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                # Wait a little and retry, useful for network streams
                time.sleep(0.1)
                continue
            with self.lock:
                self.frame = frame

    def read(self):
        # Returns the latest frame (not a copy for speed)
        with self.lock:
            return None if self.frame is None else self.frame.copy()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        self.cap.release()


camera = CameraGrabber(CAMERA_SOURCE)
camera.start()

# Utility: preprocess face ROI for model
def preprocess_roi(roi_gray):
    # expected input shape: (48,48,1), normalized
    roi_resized = cv2.resize(roi_gray, (48, 48))
    roi_norm = roi_resized.astype('float32') / 255.0
    roi_expanded = np.expand_dims(roi_norm, axis=-1)  # (48,48,1)
    roi_expanded = np.expand_dims(roi_expanded, axis=0)  # (1,48,48,1)
    return roi_expanded

# Generator that yields multipart JPEG frames for browser streaming
def gen_frames():
    while True:
        frame = camera.read()
        if frame is None:
            # send a small delay and continue
            time.sleep(0.05)
            continue

        # Work with a copy and convert to gray for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # For each face, predict emotion and annotate
        for (x, y, w, h) in faces:
            try:
                roi_gray = gray[y:y+h, x:x+w]
                roi_input = preprocess_roi(roi_gray)
                preds = model.predict(roi_input, verbose=0)
                label = EMOTIONS[np.argmax(preds)]
                confidence = float(np.max(preds))
            except Exception:
                label = "?"
                confidence = 0.0

            # Draw rectangle and put label
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            text = f"{label} ({confidence:.2f})"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Fancy frame: overlay header
        overlay_text = "Real-Time Emotion Detection"
        cv2.rectangle(frame, (0,0), (frame.shape[1], 40), (10,10,10), -1)
        cv2.putText(frame, overlay_text, (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)

        # Encode as jpeg
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()

        # Yield frame in multipart format
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


# Simple Bootstrap-based HTML template (embedded for single-file delivery)
TEMPLATE = """
<!doctype html>
<html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Emotion Detection Live</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body{ background: linear-gradient(135deg,#0f2027 0%,#203a43 50%,#2c5364 100%); color: #fff; }
        .card{ background: rgba(255,255,255,0.06); border: none; }
        .video-box{ background: #000; display:flex; align-items:center; justify-content:center; }
        .badge-conf{ background: rgba(255,255,255,0.08); padding:6px 10px; border-radius:8px; }
        footer { font-size: .9rem; opacity: .8 }
    </style>
    </head>
    <body>
    <div class="container py-4">
        <div class="row mb-3">
        <div class="col-12 text-center">
            <h1 class="display-6">Emotion Detection</h1>
            <p class="lead">Live feed with on-the-fly face detection & emotion classification</p>
        </div>
        </div>

        <div class="row g-3">
        <div class="col-md-8">
            <div class="card">
            <div class="card-body video-box">
                <img id="video-stream" src="/video_feed" alt="Live" style="width:100%; max-height:70vh; object-fit:contain;">
            </div>
            <div class="card-footer d-flex justify-content-between align-items-center">
            <div>
                <span class="badge bg-primary">Live</span>
                <span class="ms-2 badge-conf">Source: {{ camera_source }}</span>
                </div>
                <div>
                <button class="btn btn-sm btn-outline-light" id="snapshot">Take Snapshot</button>
                </div>
            </div>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card p-3">
            <h5>Info</h5>
            <p>Model: <code>{{ model_path }}</code></p>
            <p>Classes: <code>{{ emotions }}</code></p>
            <hr>
            <h6>Controls</h6>
            <p>Press <kbd>q</kbd> on server console to stop camera thread (if needed). Use the Snapshot button to download current frame.</p>
            <div id="snap-result" class="mt-3"></div>
            </div>
        </div>
        </div>

        <footer class="mt-4 text-center">Made with 3❤️ — Real-time demo</footer>
    </div>

    <script>
        document.getElementById('snapshot').addEventListener('click', async function(){
        try{
            const resp = await fetch('/snapshot');
            if(!resp.ok) throw new Error('Snapshot failed');
            const blob = await resp.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = 'snapshot.jpg';
            document.body.appendChild(a); a.click(); a.remove();
        }catch(err){
            alert('Snapshot error: ' + err.message);
        }
        });
    </script>
    </body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(TEMPLATE, model_path=MODEL_PATH, emotions=EMOTIONS, camera_source=CAMERA_SOURCE)


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/snapshot')
def snapshot():
    # Return the current frame as a JPEG for download
    frame = camera.read()
    if frame is None:
        return ("No frame", 503)
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        return ("Encode failed", 500)
    return Response(buffer.tobytes(), mimetype='image/jpeg')


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    finally:
        camera.stop()
