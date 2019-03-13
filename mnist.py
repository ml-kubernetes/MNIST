import argparse
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.layers import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--path", type=str, required=True)
    parser.add_argument("--epoch", type=int, required=True)
    parser.add_argument("--batch", type=int, required=True)
    args = parser.parse_args()

    (x_train, y_train) = tf.keras.datasets.mnist.load_data(path=args.path)[0]
    x_train = x_train[args.start:args.end]
    y_train = y_train[args.start:args.end]

    x_train = np.expand_dims(x_train, -1) / 255.0

    model = tf.keras.models.Sequential([
        Conv2D(32, (3, 3), activation='relu'),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPool2D(pool_size=(2,2)),
        Dropout(0.25),
        Flatten(),
        Dropout(0.5),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x=x_train, y=y_train, epochs=args.epoch, verbose=1, batch_size=args.batch)
