## An Example workflow

Nextflow comes with an example Nextflow workflow to help you integrate Nextpie in any Nextflow workflow. The example workflow is located in `assets/example-workflow` directory. The example workflow is a samiple workflow that takes FASTQ files as inputs and process tham using FastQC to generate quality reports per FASTQ files.

## setting an environment

First, download FastQC zipped archive and decompresse it your `$HOME` directory via terminal.

```bash
cd $HOME
wget wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.12.1.zip
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
cd Nextpie
```

Follow the instruction on Nextpie [running in a development mode](deploy-python.md). Although you can deploy Nextpie in a production environment rather easily, we are running it in development mode to keep things simple.

### Step 2: Generate a new API key
Nextpie comes with default API key `jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M`. If you have not modified this you can move to the next step.

Login to nextpie (username: admin, password: admin) and generate a new API access code code from settings page. Copy it and put the code in `example-workflow/nextflow.config`. For example in the following configuration `jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M` is an API code generated from Nextpie GUI. Replace this code by the one you generated from the settings page.

> NOTE: If you have a wrong API key in 

```groovy
params {
	//Pipeline name and version
	workflow_name = 'Test-workflow'
	workflow_ver  = '0.0.1' 
	
	// Nextpie config
	nextpie_host    = "localhost"
	nextpie_port    = 5000
	nextpie_api_key = "jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M"
	nextpie_enable  = true
}
```

### Step 3: Download input data

The folder `example-workflow/test-runs/fastq` should contain input FASTQ files for the pipeline. Download the FASTQ files from the [Google drive](https://drive.google.com/drive/folders/19PsQchNjhlfb_-USSse0Xpblh9ky76Sn) and copy them to  `example-workflow/test-runs/fastq`. Please download the files on by one and do not put them in any sub-folders.

```bash
cd nextpie/example-workflow/test-runs
ls -lah fastq
```

Once you run above bash command you should see the following files.
```
total 10G
drwxr-xr-x 2 user user 4.0K Feb 24 15:16 .
drwxr-xr-x 6 user user 4.0K Feb 24 15:39 ..
-rw-r--r-- 1 user user  131 Feb 24 15:16 README.txt
-rw-rw-r-- 1 user user 2.7G Feb 23 16:19 SRR2121687_S1_R1_001.fastq.gz
-rw-rw-r-- 1 user user 2.7G Feb 23 16:19 SRR2121687_S1_R2_001.fastq.gz
-rw-rw-r-- 1 user user 2.4G Feb 23 19:12 SRR2121688_S2_R1_001.fastq.gz
-rw-rw-r-- 1 user user 2.4G Feb 23 19:12 SRR2121688_S2_R2_001.fastq.gz
```

### Step 4: Run the workflow

Please run the following command to run the pipeline. Make sure that your located at `$HOME/nextpie/example-workflow/test-runs`. Nextflow binary is located inside `example-workflow/bin`

```bash
../bin/nextflow run \
  ../main.nf \
  --name "test_project" \
  --group "test_research_group" \
  -resume
```

Once the workflow completes successfully you will see a reply from Nextpie. In the following block `Response: {existant-processes=0, non-existant-processes=2, run-exists=1}` is the response by Nextpie. Nextpie saw this particualr pipeline run a unique run. Thus, there were

* 0 existant-processes in the database
* 2 non-existant processes (meaning data has been inserted to the database)
* 0 existing runs.


```
N E X T F L O W  ~  version 22.10.7
Launching `../main.nf` [big_easley] DSL2 - revision: 867b93c1a0
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
[5f/6076e1] process > preprocess:FastQC (SRR2121687) [100%] 2 of 2 ✔
workflow: Test-workflow
version : 0.0.1
group   : test_research_group
project : test_project
Pushing run metadata to Nextpie http://localhost:5000
Response: {existant-processes=0, non-existant-processes=2, run-exists=0}
Completed at: 31-May-2023 17:22:08
Duration    : 6m 22s
CPU hours   : 0.2
Succeeded   : 2

```
