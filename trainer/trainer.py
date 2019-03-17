import argparse
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.layers import *
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--epoch", type=int, required=True)
    parser.add_argument("--batch", type=int, required=True)
    parser.add_argument("--savemodel", type=str, required=True)
    args = parser.parse_args()

    dir_path = os.path.dirname(args.savemodel)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    mnist = np.load(args.data)
    train_x, train_y = mnist['x'], mnist['y']
    train_x = np.expand_dims(train_x, -1) / 255.0

    model = tf.keras.models.Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPool2D(pool_size=(2,2)),
        Dropout(0.25),
        Flatten(),
        Dropout(0.5),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x=train_x, y=train_y, epochs=args.epoch, verbose=1, batch_size=args.batch)
    model.save(args.savemodel)
