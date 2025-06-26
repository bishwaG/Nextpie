

## 📦 Running Nextpie Inside a Conda Environment

You can run Nextpie within a Conda environment. Follow the steps below to install Conda, set up the environment, and launch the web server.

### ✅ Step 1: Download and Install Miniconda

Download the Miniconda installer script:
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.8.3-Linux-x86_64.sh
```
Choose an installation path where you have write access. For example:
```bash
# Optional: create installation directory and change ownership
sudo mkdir -p /opt/Conda
sudo chown $USER:$USER /opt/Conda

# Set the installation path
INSTALL_PATH=/opt/Conda/miniconda3-py38_4.8.3

# Run the installer
sh Miniconda3-py38_4.8.3-Linux-x86_64.sh -p $INSTALL_PATH
```
Note: When prompted by the installer with:
```
Do you wish the installer to initialize Miniconda3 by running conda init?
```
You may answer **no** if you don’t want Conda to modify your `~/.bashrc`. However, this will change the way Conda is loaded in your terminal session. You have to export Conda binary `PATH` and load the Conda environment by executing `source activate ENV_NAME`

After installation, close the current terminal and open a new one to ensure that environment changes have taken effect.

### ✅ Step 2: Create an environment

Nextpie no longer recommends creating the Conda environment using the environment.yml file due to long setup times. Instead, install dependencies using pip.
```bash
# Clone the Nextpie repository
git clone https://github.com/bishwaG/Nextpie.git
cd Nextpie

# Create and activate a new Conda environment
conda create -n nextpie-v0.0.1 python=3.9
conda activate nextpie-v0.0.1

# Confirm pip is from the Conda environment
which pip

# Install Python dependencies using pip
pip install -r requirements/requirements.txt
```
### ✅ Step 3: Run the Gunicorn Web Server

Once dependencies are installed, you can start the Nextpie web server using Gunicorn:
```bash
gunicorn --bind 127.0.0.1:5000 run:app
```
Open your web browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

Log in using the default credentials:

- **Username:** admin
- **Password:** admin
