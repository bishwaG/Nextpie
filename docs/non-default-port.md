# Running Nextpie on a different port than 5000.

If your computer had port `5000` already in use, the same port can not be used for Nextpie. You can execute the following command to check whether the port is in use.

```
sudo netstat -tulnp | grep :5000
```
If the port is not in use, there will be no output. If the port is in use someting similr to the following will be displayed.

```
tcp        0      0 127.0.0.1:5000          0.0.0.0:*               LISTEN      489670/python3.9
```

The hassle free solution to the problem, is to termiante the service (if less cirtical) using the port `5000` and run Nextpie normally. However, if you are running a cirtical service on the port `5000`, it is wiser to run Nextpie on a different port. You can kill the process ID and the program (service) name on the last column of the above output separted by `/`. The following command can be executed to terminate the service. Please note that the processed ID and the program/service name will be different.

```
sudo kill -9 489670
```


## Changing the port for Nextpie

### Docker container
There are two approaces to run Nextpie as a docker container. You have to modify the port number in both the cases.

#### Using `docker compose`
If you are planning to run Nextpie as a docker container using the command `sudo docker compose up --build`, you have to modify the file `docker-compose.yml` in line number 8 to `"5111:5000"`. Here we are forwarding your host PC's port `5111` to docker container's port `5000`. The local port `5111` can be any port number of your choice , but make sure that it is not in use in your system. You can check it by executing the command `sudo netstat -tulnp | grep :YOUR_NEW_PORT_NUMBER`. 

Next [update the nf-nextpie config file](#updating-nf-nextpie-config).

#### Using `docker run`
If you are used to or planning to run Nextpie using the command  `sudo docker run -p 5000:5000 fimmtech/nextpie:latest`, if you have to modify the port `5000:5000` to `5111:5000`. Here we are forwarding your host PC's port `5111` to docker container's port `5000`. The local port `5111` can be any port number of your choice , but make sure that it is not in use in your system. You can check it by executing the command `sudo netstat -tulnp | grep :YOUR_NEW_PORT_NUMBER`. 

Next [update the nf-nextpie config file](#updating-nf-nextpie-config).
## Conda environment

If you are running Nextpie under a conda environment you can start Gunicorn webserver by executing the command `gunicorn --bind 127.0.0.1:5111 run:app`. Here we are running Nextpie on the host computer's port `5111`.  The local port `5111` can be any port number of your choice , but make sure that it is not in use in your system. You can check it by executing the command `sudo netstat -tulnp | grep :YOUR_NEW_PORT_NUMBER`. 

Next [update the nf-nextpie config file](#updating-nf-nextpie-config).

## Updating nf-nextpie config
We have to change the port in the plugin `nf-nextpie`'s config file as well. Nextpie has a config file `$HOME/.nextflow/plugins/nf-nextpie-0.0.1/classes/nextflow/nextpie/config.json`. The config file is created automatically only after you have run Nextflow pipeline with the parameter `-plugins nf-nextpie@0.0.1`. If the file does not exist, either run the example worklow or run any workflow with the parameter `-plugins nf-nextpie@0.0.1`. Once you have the file in the mentioned path, modify the port value `5000` to `5111` and save the file.

After changing the port from `5000` to `5111`, open your browser and go to [http://127.0.0.1:5111](http://127.0.0.1:5111). Use username `admin` and password `admin` to login.

