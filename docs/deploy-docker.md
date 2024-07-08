## Running Nextpie as a docker container
---

### Using Nextpie repository as a source
To run Nextpie as a docker container run the following commands in terminal. Before running following commands make sure that you have installed `docker` and `docker-compose` in your system and make sure that the docker daemon is running in your system. Please keep in mind that you should have root privlage to run docker containers. 

```bash
git clone https://version.helsinki.fi/fimm/nextpie.git
cd nextpie
sudo docker compose up --build
```

> **NOTE:** If you have docker-compose version `1.x.x`, you have to run `sudo docker-compose up --build` 
> **NOTE:** Add `--remove-orphans` flag to the above command in case you there are orphan containers

Open your browser and go to `http://localhost:5005`. Use username `admin` and password `admin` to login.

### Using Dockerbub as a source

Nextpie image is readily available in Dockerhub as a repository `fimmtech/nextpie`. You can conveniently pull the image and run as a container using the following commands in a terminal.

```bash
# pull the docker image
sudo docker pull fimmtech/nextpie:0.0.1

## run the image by forwarding local port 80 to container's port 5005
docker run -p 80:5005 fimmtech/nextpie:0.0.1
```

Open your browser and go to `http://localhost`. Use username `admin` and password `admin` to login.

