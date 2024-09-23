# Tapis
NSF funded web-based computing framework aimed at exposing computational research to researchers without computational expertise.

##### Higher Level Objectives
 - Programmable access to advanced resources
 - Reproduce your analysis
 - Share your data, workflows/applications, computational resources
 Without having to install your own tech stack!

Tapis is *domain agnostic* and is applied to various disciplines. The extra complexity is abstracted away from research/end users. Users build **science gateways** to interface with their research/data seamlessly through the web.

## Data Management and Code Execution
TACC uses Kubernetes in-house, but you can also use [[Docker Compose]].
There are four core parts of Tapis, originating in Tapis v1:
- /systems
- /files
- /apps
- /jobs
### How do I use Tapis?
At the lowest level, we can hit the endpoint directly using CURL:
```bash
curl -H X-Tapis-Token $token https://tacc.tapis.io/v3/apps
```
There's also a CLI:
```bash
tapis systems getSystem -systemId <my-system-id>
```
You can also use the official Python SDK **Tapipy**:
```python
>>> tp.jobs.submit(app_id='sail-fish.1.10', input_dir='data/raw/rnaseq')
```
At the highest level, you can use Tapis in web applications, like the aforementioned science gateways.


A Tapis System is an *abstraction* of a host or cluster identified by name or IP address. We can use Tapis systems to
- Store and retrieve data
- #todo I too slow

### Registering a Tapis v3 system
A system represents the following information:
- System ID
- Where the system is hosted
- Linux or S3 system
- Owner, Effective User ID of the system
A user can register Tapis v3 system either with Tapis UI, curl, or the Python/Java SDK using JSON.
In the [[Tapis#Example Sentiment Analysis|example]], we created a virtual machine host and set that as a Tapis system.

### Tapis Apps
A Tapis App represents all the information required to run a Tapis job on a Tapis system and produce useful results.
At a high level, an app represents the following information:
- App ID
- Version
- App owner
- Runtime: Docker/Singularity/ZIP
- Container Image
- Job Attributes
This information is usually represented in a JSON file.

### Tapis Jobs
Tapis Job service aims at launching applications directly on hosts (FORKED) or as jobs submitted to schedules ([[Batch Job Submission]]). The Jobs services uses the Systems, Apps, Files, and Security Kernel services to process jobs. Tapis v3 jobs are specialized to run in containerized environments.
We can also specify an email to send queue notifications to, just like `$SBATCH` jobs.
# Example: Sentiment Analysis
We're running everything in a Jupyter Notebook. It's crucial to `pip install tapipy`, but the notebook image we used already had it installed. We get the username and password from the user and use that information to authenticate the user and give them a *JSON Web Token*.
```python
from tapipy.tapis import Tapis
#Create python Tapis client for user
client = Tapis(base_url= base_url, username=username, password=password)
# *** Tapis v3: Call to Tokens API
client.get_tokens()
# Print Tapis v3 token
client.access_token
```

We create the VM host after gathering data from the user:
```python
user_id = username
system_id_vm = "taccster24-vm-" + user_id
print(system_id_vm)

# Create the system definition
exec_system_vm = {
  "id": system_id_vm,
  "description": "Test system",
  "systemType": "LINUX",
  "host": host,
  "effectiveUserId":"${apiUserId}",
  "defaultAuthnMethod": "PASSWORD",
  "rootDir": "/",
  "canExec": True,
  "jobRuntimes": [ { "runtimeType": "DOCKER" } ],
  "jobWorkingDir": "HOST_EVAL($HOME)/sharetest/workdir"
}

# Use the client to create the system in Tapis
print("****************************************************")
print("Create system: " + system_id_vm)
print("****************************************************")
client.systems.createSystem(**exec_system_vm)
```

After creating the VM host, we add our credentials that enable us to access the host:
```python
client.systems.createUserCredential(systemId=system_id_vm, userName=user_id, password=password_vm)
```

As you can see, we usually interface with our Tapis system by calling methods on the `client` Tapis object we created.

>[!Note] Transformer and NLP
> While Natural Language Processing started in the 1950s, it gained a lot of footing in [Attention is All You Need](https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf), a seminal 2017 paper that made NLP computation more performant than it had been in the past.
> We break down each work into a vector with numerical information of what order each word occurs in the sentence. This process of converting text data to numeric data is called **tokenization**.
> This is a *huge* generalization likely rife with misunderstandings on my part, but it's a good jumping off point for our example today.

We define the parameters for our app and append the app to our `client` object using the arguments we defined:
```python
app_id = "taccster24-sentiment-analysis-" + username
app_def= {
    "id": app_id,
    "version": "0.1",
    "description": "Application utilizing the sentiment analysis model from Hugging Face.",
    "jobType": "FORK",
    "runtime": "DOCKER",
    "containerImage": "tapis/sentiment-analysis:1.0.1",
    "jobAttributes": {
        "parameterSet": {
            "archiveFilter": {
                "includeLaunchFiles": False
            }
        },
        "memoryMB": 1,
        "nodeCount": 1,
        "coresPerNode": 1,
        "maxMinutes": 10
    }
}
```

We submit a job to the host to run the sentiment analysis app:
```python
pa= {
    "parameterSet": {
    "appArgs": [
            {"arg": "--sentences"},
            {"arg": "\"This is great\" \"This is not fun\""}
            
        ]
    }}

# Submit a job
job_response_vm=client.jobs.submitJob(name='sentiment analysis',description='sentiment analysis with hugging face transformer pipelines',appId=app_id,appVersion='0.1',execSystemId=system_id_vm, **pa)
```

We can view the results of our sentiment analysis
```python
client.jobs.getJobOutputDownload(jobUuid=job_uuid_vm, outputPath='results.csv')
```
Which accurately predicts the sentiment of the sentences we passed!
```
b'SENTENCE,anger,disgust,fear,joy,neutral,sadness,surprise,anger,disgust,fear,joy,neutral,sadness,surprise\r\nThis is great,0.002,0.003,0.001,0.901,0.071,0.003,0.019\r\nThis is not fun,0.032,0.076,0.004,0.003,0.031,0.845,0.008\r\n'
```
The results are difficult to read, but the first sentence ("this is great") was 90.1% joy. The second sentence ("this is not fun") was 84.5% sadness.

