# GPU Computing
## The Gist: Building a GPU Aware Container
#todo it would behoove you to read through `bert-classifier.py` and try to understand what it's doing

After running a GPU-accelerated NLP on a .csv file of a news article transcript, we get the following output:
![[Screenshot 2024-09-23 at 5.42.53 PM.png]]
#todo ask James/Erik how to interpret this data. Is this "we can say with 92% certainty that his is real news?"

---

[[Containers on High Performance Compute Clusters#Apptainer|Apptainer]] fully support GPU utilization. We can expose GPUs at runtime with the `--nv` flag. While we pull from a different set of images than [[Message Passing Interface|CPU-driven MPI jobs]], running the jobs is similar.

The base images include TensorFlow and PyTorch. We pull these images in the first stage of our Dockerfiles.

| Image                                        | Frontera/rtx | Lonestar6 |
| -------------------------------------------- | ------------ | --------- |
| tacc/tacc-ml:centos7-cuda1--tf1.15-pt1.3     | ✅            |           |
| tacc/tacc-ml:centos7-cuda-10-tf2.4-pt1.7     | ✅            |           |
| tacc/tacc-ml:centos7-cuda11-tf2.6-pt1.10     | ✅            | ✅         |
| tacc/tacc-ml:ubuntu16.04-cuda10-tf1.15-pt1.3 | ✅            |           |
| tacc.tacc-ml:ubuntu16.04-cuda10-tf2.4-pt1.7  | ✅            |           |
| tacc/tacc-ml:ubuntu20.04-cuda11-tf2.6-pt1.10 | ✅            | ✅         |
The latest version of caffe can be used on TACC systems as follows:
```bash
idev -m 60 -p rtx
module load tacc-apptainer
apptainer pull docker://nvidia/caffe:latest
apptainer exec --nv caffe_latest.sif caffe device_query -gpu 0
```

The main requirement for GPU-enabled containers to work is that the version of the NVIDIA host driver on the system supports the version of the CUDA library inside the container.

---
## TensorFlow
We install the latest version of TensorFlow as follows:
```bash
cd $SCRATCH

wget https://raw.githubusercontent.com/TACC/containers_at_tacc/master/docs/scripts/tf_test.py

apptainer pull docker://tensorflow/tensorflow:latest-gpu

apptainer exec --nv tensorflow_latest-gpu.sif python tf_test.poy
```

>[!warning] Note
> this `exec` produces a lot of warning messages from TF. We can redirect STDERR to a file
> ```bash
> 2>warnings.txt
> ```
> to clean up the output a bit
> (or `/dev/null` like a badass)
