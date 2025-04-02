## Removing test data from the databased

If you have already a [Python virtual environment](deploy-python.md) in the Nextpie root directory, skip this step. Otherwise, create a Python virtual environment and activate via terminal.

```bash
## Create a virtual environment (Unix)
python3.9 -m venv env 
source env/bin/activate
```

As a next step, change directory to Nextpie directory and run `flask clear --help` command to see the help screen (below).

```
Usage: flask clear [OPTIONS]

  Remove test data from the database.

Options:
  -g, --gid TEXT  Group IDs (separated by commas) to remove.  [required]
  --help          Show this message and exit.

```

Provide comma separated group IDs of the rows from database table `Group` to remove all the records linked to them.

```bash
flask clear --gid 1,2,3,4
```
