## An Example workflow

Nextflow comes with an example Nextflow workflow to help you integrate Nextpie in any Nextflow workflow. The example workflow is located in `assets/example-workflow` directory. The example workflow is a samiple workflow that takes FASTQ files as inputs and process tham using FastQC to generate quality reports per FASTQ files.

## setting an environment

First, download FastQC zipped archive and decompresse it your `$HOME` directory via terminal.

```bash
cd $HOME
wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.12.1.zip
unzip fastqc_v0.12.1.zip
rm -fv fastqc_v0.12.1.zip
```

Now put FastQC binary in `PATH` and run `fastqc -version`. If the command displays correct version without error you are good to go.

```bash
export PATH=$HOME/FastQC:$PATH
fastqc -version
```

## Running an example workflow

Follow these setps to run the example Nextflow workflow.


### Step 1: Download the code
To run the example pipeline along with Nextpie, download manually or use git clone in terminal.

```bash
cd $HOME
git clone https://github.com/bishwaG/Nextpie.git
cd Nextpie/
```

Follow the instruction on Nextpie [running in a development mode](deploy-python.md). Although you can deploy Nextpie in a production environment rather easily, we are running it in development mode to keep things simple.

### Step 3: Locate input data

The folder `assets/example-workflow/test-runs/fastq` should contain downsampled input FASTQ files for the pipeline.

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

### Step 4: Run the workflow

Please run the following command to run the pipeline. Make sure that your located at `$HOME/nextpie/example-workflow/test-runs`. Nextflow binary is located inside `example-workflow/bin`

> NOTE: before running the pipelien make sure that Nextpie is running under `http://localhost:5000`. For simplicity you can run it in a [development mode](deploy-python.md).

> NOTE: Make sure that you have correct version of Java (openjdk in Linux) installed. 

```bash
./nextflow run ../main.nf -plugins nf-nextpie@0.0.1\
  --fastqs 'fastq/*_R{1,2}*.fastq.gz' \
  --name "test_project" \
  --group "test_research_group" \
  -resume
```

Once the workflow completes successfully you will see a reply from Nextpie. In the following block `Response: {existant-processes=0, non-existant-processes=2, run-exists=1}` is the response by Nextpie. Nextpie saw this particualr pipeline run a unique run. Thus, there were

* 0 existant-processes in the database
* 2 non-existant processes (meaning data has been inserted to the database)
* 0 existing runs.


```
N E X T F L O W  ~  version 23.10.1
Launching `../main.nf` [focused_planck] DSL2 - revision: ca8089d2a3
===============================================================================
 Test-workflow v0.0.1
===============================================================================
Run Name       : test_project
Group          : test_research_group
FASTQs         : fastq/*_R{1,2}_*.fastq.gz
Output Dir     : ./results
===============================================================================
Do you want to continue (y/n)?y
executor >  local (2)
[52/f9e05e] process > preprocess:FastQC (SRR2121687) [100%] 2 of 2 ✔
workflow: Test-workflow
version : 0.0.1
group   : test_research_group
project : test_project
Pushing run metadata to Nextpie http://localhost:5000
Response: {message=Records inserted into the database., response=info}
Completed at: 12-Jul-2024 15:05:52
Duration    : 7m 17s
CPU hours   : 0.2
Succeeded   : 2

```
