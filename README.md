# ml-kubernetes : MNIST Example

`ml-kubernetes MNIST` is simple project that trains and predicts  `MNIST` dataset in Kubernetes cluster. This projects comducts PoC (Proof of Concept) of distributed machine learning on container environment.

## Prerequisite

All steps are done on GKE of Google Cloud Platform. You have to install ```gcloud``` comman line to use GKE.

We assume that ```gcloud``` is installed and available. If not, please refer the below link, GCP official document.

> gcloud install guide : https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu



## Creating Kubernetes Cluster on GKE

1. Create Kubernetes cluster using gcloud container clusters create command.

   ```
   $ gcloud container clusters create my-kube-cluster \
   --zone=us-central1-a \
   --cluster-version=1.11.7-gke.12 \
   --disk-size=20GB \
   --disk-type=pd-standard \
   --num-nodes=3
   ```

   You can adjust specified options, such as ```--zone```, ```--disk-size```, ```--num-nodes```, etc. 

2. Get access credential for Kubernetes.

   ```
   $ gcloud container clusters get-credentials my-kube-cluster --zone us-central1-a
   ```

   Test the kubectl command.

   ```
   $ kubectl get nodes
   NAME                                             STATUS   ROLES    AGE   VERSION
   gke-my-kube-cluster-default-pool-d0ed872d-33mt   Ready    <none>   49s   v1.11.7-gke.12
   gke-my-kube-cluster-default-pool-d0ed872d-gd42   Ready    <none>   49s   v1.11.7-gke.12
   gke-my-kube-cluster-default-pool-d0ed872d-wpv4   Ready    <none>   49s   v1.11.7-gke.12
   ```

3. Create a external disk to provide dataset to each Kubernetes node. 

   Also, you can adjust the options such as ```--size```, ```--zone```, etc.

   ```
   $ gcloud compute disks create --type=pd-standard \
   --size=1GB --zone=us-central1-a ml-kube-disk
   ```

   Congraturation! You has just created a Kubernetes cluster with 3 worker nodes.

   



## Architecture Diagram

<p align="center"><img src="https://github.com/ml-kubernetes/MNIST/raw/master/jpg/mnist-kube.png"></p>

1. ```Splitter``` split MNIST dataset into multiple dataset.

2. ```Trainer``` conducts distributed learning process in Kubernetes container.

3. ```Aggregator``` aggregates output models extracted from step 2.

4. ```Server``` container provides web page to demonstrate MNIST prediction.

   

## Quickstart of Distributed MNIST

1. First, define environment values used in distributed MNIST learning. 

2. ```
   $ export WORKER_NUMBER=3
   $ export EPOCH=2
   $ export BATCH=100
   ```

   - **$WORKER_NUMBER** : The number of workers in distributed learning. If it is set to 3, [splitter](https://github.com/ml-kubernetes/MNIST/tree/master/splitter) will split MNIST dataset into 3 files, and the 3 [trainer](https://github.com/ml-kubernetes/MNIST/tree/master/trainer)s will be spawn in each Kubernetes node as a container.
   - **$EPOCH** : // TODO
   - **$BATCH** : // TODO



2. Create NFS container to store datasets and models. It will be used as a PV, PVC in Kubernetes. ```1-nfs-deployment.yaml``` creates NFS server container to be mounted to other components, such as [splitter](https://github.com/ml-kubernetes/MNIST/tree/master/splitter),  [trainer](https://github.com/ml-kubernetes/MNIST/tree/master/trainer).

   ```
   $ kubectl apply -f 1-nfs-deployment.yaml
   $ kubectl apply -f 2-nfs-service.yaml
   ```

   Create PV and PVC using NFS container.

   ```
   $ export NFS_CLUSTER_IP=$(kubectl get svc/nfs-server -o jsonpath='{.spec.clusterIP}')
   $ cat 3-nfs-pv-pvc.yaml | sed "s/{{NFS_CLUSTER_IP}}/$NFS_CLUSTER_IP/g" | kubectl apply -f -
   ```

   **[Optional (but recommended) ]** 

   If you want to view directory of NFS server, create ```busybox``` deployment and enter into container. By default, ```index.html``` and ```lost+found``` files exist.

   ```
   $ kubectl apply -f 9999-busybox.yaml
   $ kubectl exec -it $(kubectl get pods | grep busybox | awk '{print $1}') sh
   
   / # ls /mnt
   index.html  lost+found
   / # exit
   ```

   

3. Split MNIST dataset using splitter. Splitter will create datasets, the number of $(WORKER_NUMBER)

   ```
   $ cat 4-splitter.yaml | sed "s/{{WORKER_NUMBER}}/$WORKER_NUMBER/g" | kubectl apply -f -
   ```

   To check datasets are created, check in ```busybox``` deployment. Splitted datasets exist as *.npz

   ```
   $ kubectl exec $(kubectl get pods | grep busybox | awk '{print $1}') ls /mnt/data
   0.npz
   1.npz
   2.npz
   ```

   

4. Train each dataset in Kubernetes workers. Below bash commands create [trainer](https://github.com/ml-kubernetes/MNIST/tree/master/trainer)s as deployment to train and extract neural network model. 

   ```
   $ for (( c=0; c<=($WORKER_NUMBER)-1; c++ ))
   do
     echo $(date) [INFO] "$c"th Creating th trainer in kubernetes..
     cat 5-trainer.yaml | sed "s/{{EPOCH}}/$EPOCH/g; s/{{BATCH}}/$BATCH/g; s/{{INCREMENTAL_NUMBER}}/$c/g;" | kubectl apply -f - &
   done
   ```

   After about 3 minitues, you can view the status of [trainer](https://github.com/ml-kubernetes/MNIST/tree/master/trainer) job. Status should be ```completed```.

   ```
   $ kubectl get po
   NAME                          READY   STATUS      RESTARTS   AGE
   mnist-splitter-qgkxf          0/1     Completed   0          14m
   mnist-trainer-0-g896k         0/1     Completed   0          3m
   mnist-trainer-1-6xfkg         0/1     Completed   0          3m
   mnist-trainer-2-ppnsc         0/1     Completed   0          3m
   ```

   Also you can check generated models using ```busybox``` deployment.

   ```
   $ kubectl exec $(kubectl get pods | grep busybox | awk '{print $1}') ls /mnt/model
   0-model.h5
   1-model.h5
   2-model.h5
   ```



5. Aggregate generated models into one model. Below command creates aggregator, which aggregate models into single model.

   ```
   $ kubectl apply -f 6-aggregator.yaml
   ```

   Check a aggregated model. 

   ```
   $ kubectl exec $(kubectl get pods | grep busybox | awk '{print $1}') ls /mnt
   aggregated-model.h5
   ...
   ```

   If you want to test accuracy of aggregated model, use ```9999-accuracy-test``` deployment. 

   ```
   $ kubectl apply -f 9999-accuracy-test.yaml
   $ kubectl logs --tail 1 $(kubectl get pods | grep accuracy-test | awk '{print $1}')
   10000/10000 [==============================] - 10s 997us/sample - loss: 1.2667 - acc: 0.8728
   ```



6. Create ```server``` deployment for demo. You can test MNIST prediction.

   ```
   $ kubectl apply -f 7-server.yaml
   ```

   After a few seconds, you can see the external IP to access the demo web page. Below example shows external IP is a.b.c.d, so you can access a.b.c.d:80 in web browser

   ```
   $ kubectl get svc
   NAME               TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)                      AGE
   ...
   mnist-server-svc   LoadBalancer   10.19.253.70   a.b.c.d   80:30284/TCP                 12m
   ...
   ```

   Upload a sample MNIST dataset located in ```samples/``` directory, such as 6.jpg.

   <p align="center"><img src="https://github.com/ml-kubernetes/MNIST/raw/master/jpg/upload.png" width="500" height="230"></p>

   After uploading MNIST sample, web page shows prediction result.

   <p align="center"><img src="https://github.com/ml-kubernetes/MNIST/raw/master/jpg/predict.png" width="470" height="210"></p>

## Detailed Arguments of Each Component

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
