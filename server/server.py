# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import PIL.Image as img
from flask import Flask, render_template, request
from werkzeug import secure_filename
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True)
args = parser.parse_args()

model = tf.keras.models.load_model(args.model, compile=False)
model._make_predict_function()
session = tf.keras.backend.get_session()

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        fname = secure_filename(f.filename)
        f.save(fname)

        data = np.array([np.array(img.open(fname).convert('L').resize((28, 28), img.ANTIALIAS))])
        data = np.expand_dims(data, -1) / 255.0

        with session.as_default():
            predict = model.predict(data)
            predict = np.argmax(predict[0])

        return render_template('predict.html', predict=str(predict))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
