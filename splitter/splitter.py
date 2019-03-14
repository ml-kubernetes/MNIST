import argparse
import numpy as np
import tensorflow as tf
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_container", type=int, required=True)
    parser.add_argument("--output_path", type=str, required=True)

    args = parser.parse_args()

    # Create output path if not exists
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    (train_x, train_y), (test_x, test_y) = tf.keras.datasets.mnist.load_data()
    n_data = len(train_x) // args.n_container
    for name, i in enumerate(range(0, len(train_x), n_data)):
        start, end = i, i + n_data
        np.savez(os.path.join(args.output_path, str(name)), x=train_x[start:end], y=train_y[start:end])
