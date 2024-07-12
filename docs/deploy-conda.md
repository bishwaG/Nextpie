# Running Nextpie inside a Conda environment

It is possible to run Nextpie under Conda environment. Runs the following command block to install Conda.

> NOTE: If you do not want ~/.bashrc to be modified by Conda, do not run conda init even if the conda installer suggests it.

```bash
## Download the installer
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.8.3-Linux-x86_64.sh

## Run the installer
sh Miniconda3-py38_4.8.3-Linux-x86_64.sh -p /opt/Conda/miniconda3-py38_4.8.3

## Set conda bin path
export PATH=/opt/Conda/miniconda3-py38_4.8.3/condabin:$PATH
```

Now create a new conda environment using the file `environment.yml`. The file contains dependencies with versions.

```bash
git clone https://github.com/bishwaG/Nextpie.git
cd nextpie
conda env create -f environment.yml python=3.9
```

Now load the Conda environment and run Gunicorn web server. 

```bash
source activate nextpie-v0.0.1
gunicorn --bind 0.0.0.0:8001 run:app
```

Open your browser and go to `http://localhost:80001`. Use username `admin` and password `admin` to login.
