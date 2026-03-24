from flask import Flask, render_template, request, redirect
import cv2
import numpy as np
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/swap_faces', methods=['POST'])
def swap_faces():
    if 'face1' not in request.files or 'face2' not in request.files:
        return redirect('/')

    face1 = cv2.imdecode(np.frombuffer(request.files['face1'].read(), np.uint8), cv2.IMREAD_COLOR)
    face2 = cv2.imdecode(np.frombuffer(request.files['face2'].read(), np.uint8), cv2.IMREAD_COLOR)

    swapped_img = cv2.addWeighted(face1, 0.5, face2, 0.5, 0)

    _, img_encoded = cv2.imencode('.png', swapped_img)
    return img_encoded.tobytes(), 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
