import argparse
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.layers import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--modelpath", type=str, required=True)
    parser.add_argument("--batch", type=str, default=100)
    args = parser.parse_args()

    _, (test_x, test_y) = tf.keras.datasets.mnist.load_data()

    test_x = np.expand_dims(test_x, -1) / 255.0
    model = tf.keras.models.load_model(args.modelpath, compile=False)
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    test_loss, test_acc = model.evaluate(x=test_x, y=test_y, batch_size=args.batch)