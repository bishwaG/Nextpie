
# Quick start

This quick start guide is to help user to deploy, run and test Nextpie with minimal effort.  

# Prerequisite
Make sure that you have root access to the machine you are using and you have Docker installed. For installation guide, please refer to the official [Install Docker Engine](https://docs.docker.com/engine/install/) user manual from Docker.

## Deployment
### Using Dockerhub as a source

Nextpie image is readily available in Dockerhub as a repository `fimmtech/nextpie`. You can conveniently pull the image and run as a container using the following commands in a terminal.
```bash
# pull the docker image
sudo docker pull fimmtech/nextpie:latest
```
Nextpie runs on port `5000` by default. While running Nextpie as a docker container, we forward the local (host machine) port `5000` to the docker container port `5000`. It highly recommended to check wheter the port `5000` is already in use in your machine. The following command displays information if the port is in use. It will not display anything if the port is free.

```bash
sudo netstat -tulnp | grep :5000
```
In case, the local port `5000` is already in use, please use a different port for stance `5111`. You can choose any available port, but check the availability with above command.

**When the port 5000 is free:**

Run the following command when the host port `5000` is free. In the following command we are forwarding local (host) port `5000` to the container port `5000` using the flag `-p`.
```bash
## run the image by forwarding local port 5000 to container's port 5000
sudo docker run -p 5000:5000 fimmtech/nextpie:latest
```
Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000). Use username `admin` and password `admin` to login.

**When the port 5000 is in use:**

Run the following command when the host port `5000` is in use. In the following command we are forwarding local (host) port `5111` to the container port `5000` using the flag `-p`.
```bash
## run the image by forwarding local port 5111 to container's port 5000
sudo docker run -p 5111:5000 fimmtech/nextpie:latest
```
Open your browser and go to [http://127.0.0.1:5111](http://127.0.0.1:5111). Use username `admin` and password `admin` to login.

## Running a test pipeline

Once Nextpie is deployed successfully, please refer to the [link](nextflow-workflow.md) on how to run an example workflow.

