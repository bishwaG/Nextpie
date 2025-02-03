# Nextpie

Nextpie is a reporting tool for Nextflow workflows. It uses run metadata (trace files) produced by Nextflow, puts them in database and allows a user to perform aggregate analyses. The tool is build using Python Flask and design interface from AppSeed.

Nextpie comes with with a databased populated with sample data. Thus, user can [run it using docker](docs/deploy-docker.md) without zero configuration. This enable users to evaluate the tool without big hassle of setp and configuration.

In case you decide to deploy Nextpie in a production environment please [clear the databased](docs/db-clear-test-data.md) and add [SMTP](docs/config-email.md) details in email configuration (web interface >> Settings >> SMTP settings). 

## Requirements
The code is well tested in Python `v3.9` in Redhat Exterprise Linux 8 and 9. All the python packages in requirements files under the directory `requirements` have version enforcement. Thus, it should work with other Linux distributions as long as you are able to create a Python virtual environment using mentioned version of Python packages. 

#### Minimal requirements
* Linux operating system
* Python > 3.9 (with Python virtual environment)
* Nextflow >= nextflow-23.10.1

#### Optional requirements
* Conda
* Guix
* Docker
* Gunicorn

## User manual
Nextpie can be run inside varities of software environments. Use one of the following suitable environments to deploy Nextpie.

* #### Deployment
    - [Python virtual environment](docs/deploy-python.md) (development environment)
    - [Conda environment](docs/deploy-conda.md)
    - [Guix environment](docs/deploy-guix.md)
    - [Docker](docs/deploy-docker.md)
    - [Gunicorn](docs/deploy-gunicorn.md)
    - [Waitress](docs/deploy-waitress.md) (Windows)

* #### Configurations
    - [Email](docs/config-email.md)
    - [Integrating Nextpie into Nextflow workflow](docs/configure.md)

* #### [Remove test data from the database](docs/db-clear-test-data.md)
* #### [Backup (dump) Nextpie's database (SQLite)](docs/db-dump.md)

* #### [Running an example Nextflow workflow](docs/nextflow-workflow.md)
* #### [Nextpie API](docs/api.md)
* #### [Admin page](docs/admin.md)

## Demo videos
* [Generating plots using defult interace](https://youtu.be/CrL1GM2gCLs)
