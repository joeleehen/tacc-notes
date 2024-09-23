# Containers on HPC Clusters
#### The Gist
- Docker images are *built* on your local machine
- Push docker images to Docker Hub
- `module load tacc-apptainer`
- To run a container on a big computer, either:
	- `idev` into an interactive instance and `apptainer run` from `docker://joeleehen/someContainer:verNum`
	- submit the `apptainer run` as a batch job and wait

## Apptainer
[[HPC with Linux|High Performance Computing]] systems require a slight change in how we build and run [[Docker Containers]].

We use Apptainer as a runtime for Docker containers on HPC systems.

The `shell` command opens an interactive tty within the container, a bit like a small virtual machine. This is analogous to the `-it` flag in Docker.
#note  Apptainer will mount a number of host directories (cwd, $HOME, and some system directories), and the container user is the same as on the host system

To run the default `ENTRYPOINT` or `CMD`, include the `run` command. Default behaviors are defined in the Dockerfile/Apptainer Definition file that defines the actions container performs.

The `exec` command allows for passing commands as arguments within a container.

| Apptainer                                | Docker                                                 |
| ---------------------------------------- | ------------------------------------------------------ |
| `apptainer  shell someguy.sif`           | `docker run --rm -it joeleehen/someguy:verNum`         |
| `apptainer run someguy_verNum.sif`       | `docker run --rm joeleehen/someguy:verNum`             |
| `apptainer exec someguy.sif someCommand` | `docker run --rm joeleehen/someguy:verNum someCommand` |
#note any weird docker errors (failed to get checksum, executable not recognized) are likely an error in your slurm/dockerfile. **Make sure** you have the correct **version number**.
#note sometimes `apptainer run` will fix an "executable not found" error from `apptainer exec`