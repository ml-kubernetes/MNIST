## ml-kubernetes MNIST

`ml-kubernetes MNIST` is simply project which can train or serve in distribute system. using `MNIST` data to introduce.

1. **Splitter** : [splitter](https://github.com/ml-kubernetes/MNIST/tree/master/splitter) distributes MNIST data equally by the number of contents.

   - --n_container : number of training container.

   - --savedir : saved directory path of splitted data. each data files saved `.npz` file format will be saved as number of `--n_container`.

   - Usage Example

     ```shell
     $python splitter.py --n_container 10 --savedir 
     ```

     

2. **Trainer** : [trainer](https://github.com/ml-kubernetes/MNIST/tree/master/trainer) will independently learn the data divided into each container and create a model for each container as `*.h5` file format.

   - --data : Data you want to learn from the container.

   - --epoch : number of epoch.

   - --batch : size of batch.

   - --savemodel : saved model in each container. **model format should be h5 file format**.

   - Usage Example

     ```shell
     $python train.py --data 0.npz --epoch 3 --batch 100 --savemodel model.h5
     ```

     

3. **Aggregater** : [aggregater](https://github.com/ml-kubernetes/MNIST/tree/master/aggregater) averages the stored models in each container. aggregater will find `*.h5` file format in `--dir` directory and average it.

   - --dir : In `trainer.py`, `*.h5` files saved in specific directory. This `--dir` parameter refers to its saved folder.

   - --savefile : savefile is final averaged model. **model format should be h5 file format**.

   - Usage Example

     ```shell
     $python aggregater.py --dir ./models --savefile final_model.h5
     ```

   

4. **Server** : [server](https://github.com/ml-kubernetes/MNIST/tree/master/server) serves as the final average model and serves through flasks. 

   - Usage Example

     ```python 
     model = tf.keras.models.load_model('your_model.h5', compile=False)
     ```



## ml-kubernetes Usage in GCP(Google Cloud Platform)

to do..