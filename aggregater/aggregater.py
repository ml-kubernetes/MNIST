import os
import argparse
import tensorflow as tf
from modelaverage import average

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, required=True)
    parser.add_argument("--savefile", type=str, required=True)
    args = parser.parse_args()

    dirname = os.listdir(args.dir)
    models = list()

    for file in dirname:
        filename = os.path.join(args.dir, file)
        ext = os.path.splitext(filename)[-1].strip()
        if ext == '.h5':
            models.append(filename)

    averaged_model = average(models)
    averaged_model.save(args.savefile)