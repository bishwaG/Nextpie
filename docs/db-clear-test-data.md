## Removing test data from the databased

If you want to get rid of the test data, there are two available options.

- By replacing the default SQLite databse file
- By removing test records using Flask dommand-line

## Replacing default SQLite database

Nextpie repository comes with an extra SQLite database file `assets/db-wo-test-data.sqlite3`. The database does not have any records in Group, Project, Run and Process tables. Thus, the easiest way to remove test data from the database is to replace `db.sqlite3` by `assets/db-wo-test-data.sqlite3`. Alternately, you can modify database path in `config.py` by changing `SQLALCHEMY_DATABASE_URI` value as follows. 

``python
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'assets', 'db-wo-test-data.sqlite3')
``

## Removing records using Flask CLI

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
