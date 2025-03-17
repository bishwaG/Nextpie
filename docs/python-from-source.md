# Building Python 3.9 from source
Nextpie runs on Python3.9 because of depenmdecies not available in more recent Python 3.12. You do not need a root access to a macine to build and install Python source, but you might need to install build dependencies using sudo rights.

It is recommended to updata system packages to tier latest versions.

In Ubuntu
```bash
sudo apt update -y && sudo apt upgrade -y
```
In Redhat/Fedora/Almalinux
```bash
sudo dnf -y update
```

Install Python build dependencies.

In Ubuntu
```bash
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev pkg-config wget
```
In Redhat/Fedora/Almalinux

```bash

```


Download Python 3.9, extract, build and install.
```bash
## Download and extract the source
wget https://www.python.org/ftp/python/3.9.21/Python-3.9.21.tgz
tar -xvf Python-3.9.21.tgz
cd Python-3.9.21 

## Configure
## Here we are using /opt/Python-3.9.21 as a installation path. 
## Provide a path where you have read and write access
INSTALL_APATH=/opt/Python-3.9.21
./configure --enable-optimizations --enable-shared --prefix=$INSTALL_APATH

## Build and install
make
make install
```

Make Python 3.9 available to the current shell.
```bash
export PATH=$INSTALL_APATH/bin:$PATH
export LD_LIBRARY_PATH=$INSTALL_APATH/lib

## update pip, setuptools and wheel
python3 -m pip install --upgrade pip setuptools wheel
```


