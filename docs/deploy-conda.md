
# Running Nextpie inside a Conda environment

It is possible to run Nextpie under Conda environment. Runs the following command block to install Conda. 

> NOTE: If you do not want ~/.bashrc to be modified by Conda, do not run conda init even if the conda installer suggests it.

```bash
## Download the installer
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.8.3-Linux-x86_64.sh

## Provide INSTALL_PATH where you have write access
## sudo mkdir -p /opt/Conda
## sudo chown user:user /opt/Conda
INSTALL_PATH=/opt/Conda/miniconda3-py38_4.8.3

## Type yes and press enter when asked
## Do you wish the installer to initialize Miniconda3 by running conda init?
sh Miniconda3-py38_4.8.3-Linux-x86_64.sh -p $INSTALL_PATH
```
For changes to take effect, close the current terminal and open a new terminal.

In the recent versions, we have discontinued creating a conda environment using the `environment.yml` file to install dependencies. The process can take an exceptionally long time to set up the environment. Instead of using `environment.yml` to create a conda environment, we now use Python's pip to install the dependencies.

Now create a new conda environment and install dependencies using the comands in the following code block.

```bash
git clone https://github.com/bishwaG/Nextpie.git
cd Nextpie
conda create -n nextpie-v0.0.1 python=3.9

## activate the env
conda activate nextpie-v0.0.1

## install dependency (missing in conda repo) sqlite_dump via pip
## make sure that pip you are using is from conda environment
which pip
pip3 install -r requirements/requirements.txt

```

Run Gunicorn webserver.

```bash
## run webserver
gunicorn --bind 127.0.0.1:5000 run:app
```

Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000). Use username `admin` and password `admin` to login.

