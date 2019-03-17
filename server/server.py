# -*- coding: utf-8 -*-
"""
    using flask_dropzone, license: MIT
    see LICENSE for more details. https://github.com/greyli/flask-dropzone
"""
import os
import numpy as np
import tensorflow as tf
import PIL.Image as img
from flask import Flask, render_template, request
from flask_dropzone import Dropzone

model = None

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
)

dropzone = Dropzone(app)

model = tf.keras.models.load_model('model.h5', compile=False)
model._make_predict_function()
session = tf.keras.backend.get_session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        fname = os.path.join(app.config['UPLOADED_PATH'], f.filename)

        data = np.array([np.array(img.open(fname).resize((28, 28), img.ANTIALIAS))])
        data = np.expand_dims(data, -1) / 255.0

        with session.as_default():
            predict = model.predict(data)
            predict = np.argmax(predict[0])

        return str(predict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)