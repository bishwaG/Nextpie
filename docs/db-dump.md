

## 🛢️ Backup (dump) Nextpie’s SQLite database.

To create a backup of Nextpie’s SQLite database, follow these steps:

### ✅ Step 1: Set Up Python Virtual Environment

If a [Python virtual environment](deploy-python.md) already exists in the Nextpie root directory, you can skip this step. Otherwise, create and activate a virtual environment:
```bash
# Create a virtual environment (requires Python 3.6+)
virtualenv -p python3.6 env

# Activate the environment
source env/bin/activate
```
### ✅ Step 2: Use the flask dump Command

Navigate to the root directory of the Nextpie application and run the following command to view the help for the dump operation:
```bash
flask dump –help
```
Output:
```
Usage: flask dump [OPTIONS]

  Dump Nextpie database (SQLite) to a file.

Options:
  -d, --database PATH  SQLite database path.  [required]
  -o, --out PATH       Output file path.  [required]
  --help               Show this message and exit.
```
### ✅ Step 3: Create the Backup

Provide the input database file and the output destination file for the backup. For example:
```bash
flask dump --database db.sqlite3 --out db-snapshot-240625.txt
```
Replace `db.sqlite3` with your actual database file name and `db-snapshot-240625.txt` with your preferred output file name.

### ✅ Step 4: Store the Backup Securely

Copy the generated backup text file to a secure location. This file contains the contents of your Nextpie database and should be protected accordingly.
