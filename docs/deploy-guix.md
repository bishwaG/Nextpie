# Running Nextpie using Guix

Nextpie can be run in Guix as well. Please refer to [Guix installation guide](https://guix.gnu.org/manual/en/html_node/Binary-Installation.html) to install in your system. Please note that Guix instalaltion requires root privlage. 

THe the following code block to create a Guix environment for Nextpie. 
```bash
git clone https://github.com/bishwaG/Nextpie.git
cd Nextpie
guix shell -m manifest.scm
```

After running above code block you will see `[env]` in your prompt. This tells that the Guix environment is active. Since Guix repository does not have all the dependencies of Nextpie, we install via `pip3`. 

First make sure that `pip3` which in `PATH` is not a system-wide installed one.
```bash
which pip3
```

Now, Install the dependencies.

```bash
pip3 install -r requirements/requirements.txt
```

Once the dependencies are installed successfully, run the following command to run Nextpie under Gunicorn wer server.

```bash
gunicorn --bind 0.0.0.0:8001 run:app./run-app.sh
```

Open your browser and go to `http://localhost:80001`. Use username `admin` and password `admin` to login.
