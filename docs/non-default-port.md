


## Running Nextpie on a Different Port than 5000

If your computer already has port `5000` in use, it cannot be used for running Nextpie. To check whether the port is in use, execute the following command:
```bash
sudo netstat -tulnp | grep :5000
```
If the port is not in use, there will be no output. If it is in use, you will see an output similar to the following:
```bash
tcp 0 0 127.0.0.1:5000 0.0.0.0:* LISTEN 489670/python3.9
```
The simplest solution is to terminate the service using port `5000` (if it’s non-critical) and run Nextpie normally. However, if the service using port `5000` is critical, it is preferable to run Nextpie on a different port. You can terminate the process using the process ID and program name shown in the last column of the output above. Use the following command (replace the ID accordingly):
```bash
sudo kill -9 489670
```
### ✅ Step 1: Changing the Port for Nextpie

#### 1.1 Docker Container

There are two ways to run Nextpie as a Docker container. In both cases, you will need to modify the port number.

**Using docker compose**

If you plan to use the command sudo docker compose up `--build`, you will need to edit the `docker-compose.yml` file. Change line 8 to:
```
"5111:5000"
```
This forwards your host computer’s port `5111` to the container’s port `5000`. You can use any available port number instead of `5111`, but ensure that it is not already in use. Check the availability with:
```bash
sudo netstat -tulnp | grep :YOUR_NEW_PORT_NUMBER
```
**Using docker run**

If you are using the command:
```bash
sudo docker run -p 5000:5000 fimmtech/nextpie:latest
```
Replace 5000:5000 with 5111:5000 to use a different host port:
```bash
sudo docker run -p 5111:5000 fimmtech/nextpie:latest
```
Again, ensure that the selected host port is not in use. Check with:
```bash
sudo netstat -tulnp | grep :YOUR_NEW_PORT_NUMBER
```
#### 1.2 Conda/Guix Environment

If you are running Nextpie in a Conda or Guix environment, you can start the Gunicorn web server with:
```bash
gunicorn --bind 127.0.0.1:5111 run:app
```
This starts Nextpie on port `5111`. As before, you can choose any available port. Check the availability with:
```bash
sudo netstat -tulnp | grep :YOUR_NEW_PORT_NUMBER
```
#### 1.3 Python environment

If you are running Nextpie in a python (development environment), run the following command to start Nextpie. Note that the default port `5000` has been changed to `5111`.
```bash
flask run --host=127.0.0.1 --port=5111
```
As before, you can choose any available port. Check availability with:
```bash
sudo netstat -tulnp | grep :YOUR_NEW_PORT_NUMBER
```
### ✅  Step 2: Updating nf-nextpie Config

You will also need to update the port in the nf-nextpie plugin’s config file, located at:
```
$HOME/.nextflow/plugins/nf-nextpie-0.0.1/classes/nextflow/nextpie/config.json
```
This file is automatically created after running any Nextflow pipeline with the parameter:
```
-plugins nf-nextpie@0.0.1 
```
If the file does not exist, run the example workflow or any workflow using the above plugin parameter. Once the file is available, open it, change the port from `5000` to `5111`, and save it.

After updating the configuration, open your browser and navigate to: [http://127.0.0.1:5111](http://127.0.0.1:5111).

Log in using:

* **Username:** admin
* **Password:** admin
