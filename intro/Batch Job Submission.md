# Batch Job Submission
We *submit* a *batch* of *jobs* to perform on the compute nodes of [[HPC with Linux#Lonestar6|Lonestar6]]. The actual submission is a simple `.slurm` file that explains the resources we need and the commands we wish to run for or job.

There are different queues on Lonestar6; it's important to choose the right queue for your job based on queue limitations. RTFM [here](https://docs.tacc.utexas.edu/hpc/lonestar6/#table5)!

## Example
`.slurm` files look a lot like simple BASH scripts:
```bash
!/bin/bash
----------------------------------------------------
Example SLURM job script to run applications on
TACCs Lonestar6 system.
----------------------------------------------------
#SBATCH -J                # Job name
#SBATCH -o                # Name of stdout output file
#SBATCH -e                # Name of stderr er
#SBATCH -p                # Queue (partition) name
#SBATCH -N                # Total # of nodes (must be 1 for serial)
#SBATCH -n                # Total # of mpi tasks (should be 1 for serial)
#SBATCH -t                # Run time (hh:mm:ss)
#SBATCH -A                # Project/Allocation name (req'd if you have more than 1)

# Everything below here should be Linux commands
```

>[!error] Note
> if you leave any `#SBATCH` argument blank (as provided in many of templates `SBATCH -A    `), sbatch will NOT queue your job

Say we want to use `autodock_vina` to check how well a small molecule ligand fits within a protein binding site. All the data required for this job is in a subdirectory called `data/`
We fill out `job.slurm` to request the resources we need.
>[!example] Note
> Estimating how many nodes/mpi tasks you'll need for a given task takes time. You'll need to guess and check as you go to get a feel for how much you need. Reading documentation for the tools you use will help!

We begin by specifying the `SBATCH` parameters for the job we want to queue. Afterwards, we provide instructions to the compute node on how to run our job. This will change depending on what tools or apps you're using.

Here's the `job.slurm` file we've written for this example:
```bash
#SBATCH -j vina_job
#SBATCH -o vina_job.o%j
#SBATCH -e vina_job.e%j
#SBATCH -p development
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 00:10:00

# everything below here should be linux commands
echo "starting at:"
date

module list
module use /work/03439/wallen/public/modulefiles
module load autodock_vina/1.2.3
module list

cd data/
vina --config configuration_file.txt --out ../results/output_ligands.pdbqt

echo "ending at:"
date
```

