

# Building Python 3.9 from source

Nextpie runs on Python3.9 because of dependencies not available in the more recent Python 3.12. You do not need root access to a machine to build and install Python source, but you may need to install build dependencies using sudo rights.

## 🎥Instruction video

Please refer to this instruction video on how to build Python source from [Youtube](https://youtu.be/VbsuMxXdtTk).

## ⬆️ Update packages

It is recommended to update system packages to their latest versions.

In Ubuntu
```bash
sudo apt update -y  **&&**  sudo apt upgrade -y
```
In Redhat/Fedora/Almalinux
```bash
sudo dnf -y update
```
## 📥 Install Python build dependencies.

In Ubuntu
```bash
sudo apt install build-essential \
  zlib1g-dev \
  libncurses5-dev \
  libgdbm-dev \
  libnss3-dev \
  libssl-dev \
  libreadline-dev \
  libffi-dev \
  pkg-config \
  python3-virtualenv \
  libbz2-dev \
  libsqlite3-dev \
  python3-setuptools \
  python3-dev \
  python3-wheel \
  git wget
```
In Redhat/Fedora/Almalinux
```bash
sudo dnf -y install openssl-devel \
  bzip2-devel \
  libffi-devel \
  wget \
  python3-virtualenv   
  
sudo dnf -y groupinstall "Development Tools"
```
## 🛠️ Build and install

Download Python 3.9, extract, build and install.
```bash
## Download and extract the source
wget https://www.python.org/ftp/python/3.9.21/Python-3.9.21.tgz  
tar  -xvf Python-3.9.21.tgz  
cd Python-3.9.21  
  
## Configure
## Here we are using /opt/Python-3.9.21 as an installation path.
## Provide a path where you have read and write access.
## Note that you do not need sudo rights to build and install Python
# sudo mkdir /opt/Python-3.9.21
# sudo chown $USER:$USER /opt/Python-3.9.21
INSTALL_PATH=/opt/Python-3.9.21  
./configure  --enable-optimizations  --enable-shared  --prefix=$INSTALL_PATH  
  
## Build and install
make  
make install

Make Python 3.9 available to the current shell.

export  PATH=$INSTALL_PATH/bin:$PATH  
export  LD_LIBRARY_PATH=$INSTALL_PATH/lib  
  
## update pip, setuptools and wheel
python3  -m pip install --upgrade pip setuptools wheel
```
