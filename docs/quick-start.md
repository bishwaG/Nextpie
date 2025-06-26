

# Quick Start

This quick start guide will help you deploy, run, and test **Nextpie** with minimal effort.

## Prerequisites

Ensure you have **root access** to your machine and that **Docker** is installed. For installation instructions, please refer to Docker’s official guide: [Install Docker Engine](https://docs.docker.com/engine/install/).

## ✅ Step 1. Deployment

### Pull and Run the Docker Container

The Nextpie Docker image is available on Docker Hub under the repository:  

[**fimmtech/nextpie**](https://hub.docker.com/r/fimmtech/nextpie)

You can pull the image and run it as a container using the following commands:
```bash
# Pull the Docker image 
sudo docker pull fimmtech/nextpie:latest
```
Nextpie runs on port `5000` by default. When launching the container, the local (host) port `5000` is forwarded to the container’s port `5000`.

Before proceeding, it is a good idea to check whether port `5000` is already in use:
```bash
sudo netstat -tulnp  **|**  grep :5000
```
If the port is free, proceed as shown below. Otherwise, use an alternative port such as `5111`.

#### ☑️ When Port 5000 is Available

Run the following command to map host port `5000` to container port `5000`:
```bash
sudo docker run -p 5000:5000 fimmtech/nextpie:latest
```
Now, open your browser and visit:  
[http://127.0.0.1:5000](http://127.0.0.1:5000/)

Use the following default credentials to log in:

-   **Username:** admin  
-   **Password:** admin
    

#### ❗ When Port 5000 is in Use

If port `5000` is already taken, you can use an alternative, such as `5111`:
```bash
sudo docker run -p 5111:5000 fimmtech/nextpie:latest
```
Open your browser and go to:  
[http://127.0.0.1:5111](http://127.0.0.1:5111/)

Use the same credentials:

-   **Username:** admin  
-   **Password:** admin
    

## ✅ Step 2. Running a Test Pipeline

Once Nextpie is up and running, follow the [example workflow guide](nextflow-workflow.md) to run a test Nextflow pipeline and see how the reporting works.
