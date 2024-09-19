# HPC with Linux
## Architecture
We work with two different types of nodes: **login** nodes and *compute* nodes. We log in to the login nodes (🤯🤯🤯) and *queue* a job to a compute node.
![[Screenshot 2024-09-19 at 1.45.59 PM.png|550]]
## Lonestar6
Logging in to Lonestar6 is done through the terminal:
``` bash
ssh username@ls6.tacc.utexas.edu
(enter password)
(enter 6-digit token)
```
Successfully logging in displays a welcome message with information about compute utilization and limits.

>[!tip] A Note About Quotas
> Once you get close to your disk usage quota, you'll experience performance issues that impact you *and* the work of others.
> For example, if you're nearing your quota on `$WORK` and keep trying to write to `$WORK`, you stress that file system.
> You can also monitor your disk quotas/other TACC project balances with
> ```[ls6]$ /usr/local/etc/taccinfo```

```
$WORK: /work/10287/joeleehen/ls6
$SCRATCH: /scratch/10287/joeleehen
```
To transfer files from the local machine to Lonestar6 (`$WORK` directory), we use  `scp`:
`scp my_file joeleehen@ls6.tacc.utexas.edu:/work/10287/joeleehen/ls6`
This is run from the *local machine*!
We can also recursively copy full directories using `rsync`:
``` bash
rsync -azv local remote
rsync -azv remote local
```

### Batch Job Submission
We don't run applications on login nodes; the work is too resource-intensive and will interrupt what other people are doing. Instead, we write a **short text file** explaining the resources we need and the commands for running the application. We then submit that text file to a queue to run on compute nodes. This is called [[Batch Job Submission]]
