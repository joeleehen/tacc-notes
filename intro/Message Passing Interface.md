# Message Passing Interface (MPI)
### The Gist
#### Interactive Mode
Allocating a single 8-task node on the development queue
```bash
idev -m 60 -p development -N 1 -n 8
```
We pull containers in `$SCRATCH` so we don't go over our `$HOME` quota.
**CHANGE TO SCRATCH BEFORE PULLING**
After pulling, we can run our container:
###### Sequentially
```bash
ibrun -n 1 apptainer run someguy_verNum.sif
```
###### Distributed over multiple nodes
```bash
ibrun apptainer run someguy_verNum.sif
```
###### Distributed with fewer tasks
```bash
ibrun apptainer run someguy_verNum.sif
```

#note the `-n` flag will configure the number of processes allocated for the job

#### [[Batch Job Submission]]
Running parallelized batch jobs isn't much different than sequential batch jobs. You have to first pull the container to your `$SCRATCH` directory, but is otherwise familiar:
```bash
#!/bin/bash

#SBATCH -J calculate-pi-mpi
#SBATCH -j calculate-pi-mpi.%j
#SBATCH -p development
#SBATCH -N 1
#SBATCH -n 8
#SBATCH -t 00:10:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jlh7459@my.utexas.edu

module load tacc-apptainer
cd $SCRATCH
ibrun apptainer run pi-estimator_0.1-mpi.sif pi-mpi.py 10000000
```

Multiple computers/nodes need to synchronize with each other when working on a common problem. *Message Passing Interface* defines a standard suite of functions for synchronization, exchanging data, and providing command and control over the entire parallel cluster.

Since MPI isn't an exact standard, there are mismatches between software/hardware implementations. You want the version of the MPI **inside the container** to be the same version *or newer* than **the host**. This means there are additional requirements for the host system.

TACC uses a curated set of Docker images to use in our own containers. This should ensure compatibility with MPI interfaces.

| Image                                | Frontera | Lonestar6 | Local Dev |
| ------------------------------------ | -------- | --------- | --------- |
| tacc/tacc-centos7-mvapich2.3-ib      | ✔️       | ✔️        | ✔️        |
| tacc/tacc-centos7-impi19.0.7-common  | ✔️       | ✔️        | ✔️        |
| tacc/tacc-ubuntu18-mvapich2.3-ib     | ✔️       | ✔️        | ✔️        |
| tacc/tacc-ubuntu18-impi19.0.7-common | ✔️       | ✔️        | ✔️        |
>[!warning] Warning
> For now, building from an Intel-based base image will throw some weird-ass GPG check fail error. To get around this, pass an `apt-get` flag to allow for insecure/downgraded libraries:
> ```bash
> apt-get -o Acquire::AllowInsecureRepositories=true -o Acquire::AllowDowngradeToInsecureRepositories=true
> ```
> There's also a brand new version of mpi4py that throws a weird Cython error. Specify an older version to avoid build fails:
> ```bash
> pip3 install mpi4py==3.1.4
>```
> 

>[!note]
> The Apptainer version of these containers should be invoked with `apptainer run` on HPC.

>[!Example] Another note
> We usually differentiate MPI containers either by tag:
> ``` bash
> docker build -t joeleehen/someContainer:verNum-mpi
> ```
> or by simply naming the container differently
> ```bash
> docker build -t joeleehen/someContainer-mpi:verNum
> ```
## MPI Jargon
**Comm**: communicator objects that connect groups of processes in MPI. Communicator commands give a contained process an independent identifier, arranged as an ordered topology. `MPI.COMM_WORLD` is the name of the default MPI communicator (the collection of all processes).
Almost every MPI command needs to provide a communicator as input argument.
**Rank**: indexed starting at 0, rank is an integer identifier issued for each process in a communicator. *Processes* are the actual instances of the program that are running; *rank* is merely the $\underline{\text{identifier}}$ for that instance. `MPI.COMM_WORLD.Get_rank()` 
**Size**: the number of processes/ranks in a communicator. For `MPI.COMM_WORLD.Get_size()`, this returns the total number of processes.
