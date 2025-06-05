# Removing test data from the databased

If you want to get rid of the test data, there are two available options.

- Via the API
- By replacing the default SQLite databse file
- By removing test records using Flask dommand-line


## Removing the records using the API

To delete all the records associated to groups, you can provide comma separated group IDs using `/delete-records` in the API endpoint `http://127.0.0.1:5000/api/v1.0`. This is not limited to test data removal only.

![](images/remove-data-by-gid.png)

Make sure that you have deployed Nextpie and it is running. 

### Step 1:

- Go to [http://127.0.0.1:5000/api/v1.0](http://127.0.0.1:5000/api/v1.0)
- Click **Authorize** button and provide the default API key `jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M`, if you have not created a new API key from the Nextpie's web interface. A newly created API key will always overwrite the old one.

### Step 2: 

- Click the **Default namespace** and expand it.
- Click **/delete-records** and expand it.
- Click **Try it out** button. This will enable **GroupID** textfield and also shows **Execute** button.

### Step 3:

- Provide comma separated group IDs you would like to remove. If you want to remove only the test data, provide group IDs `1, 2, 3, 4, 5, 6, 7, 8, 10, 11`. You can easily get group IDs from Nextpie's web interface (Database >> Group).

### Step 4:

- Press the **Execute** button.

This will deleted all the records (project, run, and process) from the database for the provided groups.

## Replacing default SQLite database

> NOTE: This method does not work if you have deployed Nextpie as a Docker container.

Nextpie repository comes with an extra SQLite database file `assets/db-wo-test-data.sqlite3`. The database does not have any records in Group, Project, Run and Process tables. Thus, the easiest way to remove test data from the database is to replace `db.sqlite3` by `assets/db-wo-test-data.sqlite3`. Alternately, you can modify database path in `config.py` by changing `SQLALCHEMY_DATABASE_URI` value as follows. 

``python
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'assets', 'db-wo-test-data.sqlite3')
``

## Removing records using Flask CLI

> NOTE: This method does not work if you have deployed Nextpie as a Docker container.

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
