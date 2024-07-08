## Backup (dump) Nextpie's SQLite database.

If you have already a [Python virtual environment](deploy-python.md) in the Nextpie root directory, skip this step. Otherwise, create a Python virtual environment and activate via terminal.

```bash
## Create a virtual environment (Unix)
virtualenv -p python3.6 env
source env/bin/activate
```

As a next step, change directory to Nextpie directory and run `flask dump --help` command to see the help screen (below).

```
Usage: flask dump [OPTIONS]

  Dump Nextpie database (SQLite) to a file.

Options:
  -d, --database PATH  SQLite database path.  [required]
  -o, --out PATH       Output file path.  [required]
  --help               Show this message and exit.


```

Provide comma provide input SQLite databse file and output text file to backup the database.

```bash
flask dump --database db.sqlite3 --out db-snapshot-ddmmyy.txt
```

Copy the text file to a safe location.
