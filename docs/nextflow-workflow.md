


## An Example workflow

Nextpie comes with an example Nextflow workflow to help you integrate Nextpie into any Nextflow workflow. The example workflow is located in `assets/example-workflow` directory. The example is a simple workflow that takes FASTQ files as inputs and process them using FastQC to generate quality reports per FASTQ files.

### Prerequisite
Before proceeding, ensure that you have Nextpie up and running. You can adopt one of the many deployment methods mentioned on the [main page](../README.md).

## setting an environment

First, download the FastQC zipped archive and decompress it in your `$HOME` directory via a terminal.

```bash
cd $HOME
wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.12.1.zip
unzip fastqc_v0.12.1.zip
rm -fv fastqc_v0.12.1.zip
```

Now put the FastQC binary in your `PATH` and run `fastqc -version`. If the command displays the correct version without an error you are ready to continue.

```bash
export PATH=$HOME/FastQC:$PATH
fastqc -version
```
Make sure that you have the correct version of Java installed. In Ubuntu `24.04.2 LTS`, installing Java version 17 will be sufficient for both FastQC and Nextflow `24.10.4`.
```bash
sudo apt install openjdk-17-jre-headless
```

## Running an example workflow

Follow these steps to run the example Nextflow workflow.


### ✅ Step 1: Download the code
To run the example pipeline along with Nextpie, download it manually or use `git clone` in a terminal.

```bash
cd $HOME
git clone https://github.com/bishwaG/Nextpie.git
cd Nextpie/
```

### ✅ Step 2: Locate input data

The folder `assets/example-workflow/test-runs/fastq` should contain down-sampled input FASTQ files for the pipeline.

```bash
cd assets/example-workflow/test-runs
ls -lah fastq
```

Once you run above bash command you should see the following files.
```
total 4.7M
drwxr-xr-x 2 user user 4.0K Mar 12 19:18 .
drwxr-xr-x 8 user user 4.0K Mar  3 16:02 ..
-rw-r--r-- 1 user user  294 Mar  2 21:50 README.md
-rw-r--r-- 1 user user 1.2M Mar  2 15:25 SRR2121687_S1_R1_001.fastq.gz
-rw-r--r-- 1 user user 1.2M Mar  2 15:26 SRR2121687_S1_R2_001.fastq.gz
-rw-r--r-- 1 user user 1.2M Mar  2 15:27 SRR2121688_S2_R1_001.fastq.gz
-rw-r--r-- 1 user user 1.2M Mar  2 15:27 SRR2121688_S2_R2_001.fastq.gz
```

### ✅ Step 3: Run the workflow

Please run the following command to run the pipeline. Ensure that you are located at `$HOME/nextpie/example-workflow/test-runs`. The Nextflow binary is located inside `example-workflow/bin`.

> ⚠️ NOTE: before running the pipeline make sure that Nextpie is running under `http://localhost:5000`. For simplicity you can run it in a [docker container](deploy-docker.md). If you do not have sudo right to run a docker container, deploy Nextpie using a [Conda](deploy-conda.md) or [Python virtual environment](deploy-python.md).

> ⚠️ NOTE: If you are [running Nextpie on a non-default port](non-default-port.md),  please remember to update `port` in nf-nextpie plugin's config file `$HOME/.nextflow/plugins/nf-nextpie-0.0.1/classes/nextflow/nextpie/config.json`.

> ⚠️ NOTE: Make sure that you have correct version of Java (openjdk in Linux) installed for Nextlow. 

> ⚠️ Ensure that `trace.enabled=true` is set in your Nextlow workflow’s `nextflow.config` file.

```bash
## limit heap size for nextflow
NXF_OPTS='-Xms1g -Xmx1g'
_JAVA_OPTIONS='-Xms1g -Xmx4g'

./nextflow run ../main.nf \
  -plugins nf-nextpie@0.0.2 \
  --fastqs 'fastq/*_R{1,2}*.fastq.gz' \
  --name "test_project" \
  --group "test_research_group"
```

Once the workflow completes successfully you will see a reply from Nextpie. In the following block `{"message":"Records are inserted into the database (2 new processes).","response":"success"}` is the response by Nextpie.

```bash
 N E X T F L O W   ~  version 24.10.4

Launching `../main.nf` [grave_hilbert] DSL2 - revision: 64da441873

[NEXTPIE] Pipeline name Test-pipeline and version label 2.1.0 found in manifest scope.
[NEXTPIE] The variables workflow_name and workflow_ver from the params scope will be ignored if they exist.
[NEXTPIE] Config file: /home/bishwa/.nextflow/plugins/nf-nextpie-0.0.2/classes/nextflow/nextpie/config.json
===============================================================================
 PIPELINE: Test-pipeline VERSION: 2.1.0
===============================================================================
Run Name       : test_project
Group          : test_research_group
FASTQs         : fastq/*_R{1,2}*.fastq.gz
Output Dir     : ./results
===============================================================================
Do you want to continue (y/n)?y
executor >  local (2)
[55/e0d436] preprocess:FastQC (SRR2121687) [100%] 2 of 2 ✔
Workflow complete ☑️ 
[NEXTPIE] Uploading usage data!
[NEXTPIE] Trace file: ./results/pipeline_info/Trace.txt
[NEXTPIE] URI: http://localhost:5000/api/v1.0/upload-data
[NEXTPIE] Response:
 {
  "message": "Records are inserted into the database (2 new processes).",
  "response": "success"
}

```
