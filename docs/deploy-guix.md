

## 📦 Running Nextpie Using Guix

Nextpie can also be run within a Guix environment. To get started, please refer to the official [Guix installation guide](https://guix.gnu.org/manual/en/html_node/Installation.html) to install Guix on your system. Note that Guix installation requires root privileges.

> ⚠️ Important: Guix has only been tested on Red Hat Linux 9.5 and is not tested on Ubuntu or other distributions.

### Setting Up the Guix Environment for Nextpie

### ✅ Step 1: Clone the Nextpie repository and navigate to its directory: 
```bash
git clone https://github.com/bishwaG/Nextpie.git 
cd Nextpie
```
### ✅ Step 2: Create and activate the Guix environment by running: 
```bash
guix shell -m manifest.scm
```
After this command executes, your terminal prompt will display [env], indicating the Guix environment is active.

### Installing Dependencies

Because the Guix repository does not include all of Nextpie’s dependencies, you will need to install the remaining dependencies using pip3.

- First, verify that the pip3 in your current PATH is not the system-wide installation by running: 
```bash
which pip3
```
- Then install dependencies from the requirements file: pip3 install -r requirements/requirements.txt

### Running Nextpie

- Ensure the gunicorn being used is the one from inside the Guix environment and not system-wide: 
```bash
which gunicorn 
```
-  Run the Gunicorn web server on port 5000: 
```bash
gunicorn --bind 127.0.0.1:5000 run:app
```
Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000). 

Use the default login credentials:

**Username:** admin
**Password:** admin

### Stopping and Exiting

* Press **Ctrl+C** in the terminal to terminate the Gunicorn server.
* Press **Ctrl+D** to deactivate the Guix environment.
