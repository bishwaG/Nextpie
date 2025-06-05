# Quick Start

This quick start guide will help you deploy, run, and test Nextpie with minimal effort.

# 1. Prerequisites

Ensure that you have root access to the machine and that Docker is installed. For installation instructions, please refer to the official [Install Docker Engine](https://docs.docker.com/engine/install/) guide from Docker.

## 2. Deployment

### 2.1 Pulling an running a (Docker) container image

The Nextpie image is available on Docker Hub under the repository [fimmtech/nextpie](https://hub.docker.com/repository/docker/fimmtech/nextpie/general). You can easily pull the image and run it as a container using the following commands in a terminal:

```bash
# Pull the Docker image
sudo docker pull fimmtech/nextpie:latest
```

Nextpie runs on port `5000` by default. When running Nextpie as a Docker container, the local (host machine) port `5000` is forwarded to the container's port `5000`. It is highly recommended to check whether port `5000` is already in use on your machine. The following command will display information if the port is in use; otherwise, it will return nothing.

```bash
sudo netstat -tulnp | grep :5000
```

If port `5000` is already in use, please use a different port, such as `5111`. You can choose any available port, but make sure to check its availability using the command above.

#### When port 5000 is Free

Run the following command when host port `5000` is free. This command forwards the local port `5000` to the container's port `5000` using the `-p` flag:

```bash
# Run the container with local port 5000 forwarded to container port 5000
sudo docker run -p 5000:5000 fimmtech/nextpie:latest
```

Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000). Use the following credentials to log in:

* **Username:** `admin`
* **Password:** `admin`

#### When port 5000 is in Use

Run the following command when host port `5000` is already in use. This command forwards local port `5111` to the container's port `5000`:

```bash
# Run the container with local port 5111 forwarded to container port 5000
sudo docker run -p 5111:5000 fimmtech/nextpie:latest
```

Open your browser and go to [http://127.0.0.1:5111](http://127.0.0.1:5111). Use the following credentials to log in:

* **Username:** `admin`
* **Password:** `admin`

## 3. Running a Test Pipeline

Once Nextpie has been successfully deployed, refer to the [example workflow guide](nextflow-workflow.md) to run a test pipeline.

