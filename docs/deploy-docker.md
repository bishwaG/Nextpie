


## 🐳 Running Nextpie as a Docker Container

Nextpie can be deployed easily using Docker. Below are two approaches: building from source, or pulling from Docker Hub.

✅ Prerequisites
- Root or sudo access
- Docker and Docker Compose installed
- Docker daemon running

🔗 For installation, refer to the official Docker installation guide: https://docs.docker.com/engine/install/

### 🎥 Instructional video

You may refer to the instructional video available on [YouTube](https://youtu.be/kmLNcgQN33I).


### ✅ Option 1: Using Docker Hub

You can also run Nextpie directly from the prebuilt Docker image hosted on Docker Hub.

1. Pull the latest image: 
```bash
# pull the docker image
sudo docker pull fimmtech/nextpie:latest
```
2. Run the container by exposing the correct port: 
```bash 
## run the image by forwarding local port 5000 to container's port 5000
sudo docker run -p 5000:5000 fimmtech/nextpie:latest
```
3. Visit http://127.0.0.1:5000 in your browser and log in using the default credentials.

### ✅ Option 2: Using the Nextpie Repository

1. Clone the Nextpie repository and navigate into the directory: 
```bash
git clone https://github.com/bishwaG/Nextpie.git 
cd Nextpie
```
2. Build and run the container using Docker Compose: 
```bash
sudo docker compose up --build
```

📝 Note:

- If you’re using Docker Compose `v1.x.x`, use `sudo docker-compose up --build` instead.
- Add `--remove-orphans` if you have leftover containers from previous builds.

3. Once the container is running, open your browser and visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

Log in using the default credentials:
- **Username:** admin
-  **Password:** admin
### 🔧 Useful Docker Commands

These Docker commands can help with troubleshooting or managing containers:

```bash
## list all docker images
sudo docker images -a

## delete a docker image
sudo docker rmi [IMAGE ID]

## list all containers
docker ps -a

## Stop a container
docker stop [CONTAINER ID]

## remove a container 
docker rm --force [CONTAINER ID]

## SSH to a container
docker exec -it [CONTINER NAME] /bin/bash
```
