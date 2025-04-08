
## An Example workflow

Nextflow comes with an example Nextflow workflow to explore Nextpie features. The example workflow is located in `assets/example-workflow` directory. Please refer to `assets/example-workflow/test-runs/run-analysis.sh` script.

## Configure Nextflow pipeline for Nextpie

Nextpie has a client plugin named [nf-nextpie](https://github.com/bishwaG/nf-nextpie). Once you export the environment variable `NXF_PLUGINS_TEST_REPOSITORY` (with the value shown in the code block below) and Nextflow command-line option`-plugins nf-nextpie@0.0.1`, Nextflow will automatically download the plugin during runtime and stores in `$HOME/.nextflow/plugins/nf-nextpie-0.0.1`. This greatly minimizes configuration hassles. Currently, `nf-nextpie` plugin is not in Nextflow's plugin repository. Once it is available in the Nextflow's public repository, you do not even have to export `NXF_PLUGINS_TEST_REPOSITORY` variable.

```bash
## Provide nf-nextplugin location
export NXF_PLUGINS_TEST_REPOSITORY="https://github.com/bishwaG/nf-nextpie/releases/download/0.0.1/nf-nextpie-0.0.1-meta.json"

## Run Nextflow using -plugins command-line parameter
./nextflow run ../main.nf -plugins nf-nextpie@0.0.1  ....
```
When pipeline completes, `workflow.complete` triggers `nf-nextpie` to upload usage data to Nextpie.

The plugin comes with a default config file. The file is located at `$HOME/.nextflow/plugins/nf-nextpie-0.0.1/classes/nextflow/nextpie/config.json` in the local dowload copy. The config file contains enties for Nextpie host, port in which Nextpie in running in the host, and an API key to connect to Nextpie host.

config.json:
```
{
  "host": "localhost",
  "port": 5005,
  "api-key": "jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M"
}
```

> NOTE: For security reasons it is highly recommended not to use the default `api-key` in a production systems.

## Firewall configuration

If you have a firewall running in a machine where Nextpie is running, it is essential to open the port on which Nextpie is listening/running. Nextpie run by default on port `5000`. The port can be changed according to your need. If you deploy Nextpie into a production you could modify the port to `8080` or `80` (may require root access). Please refer to [Gunicorn](deploy-gunicorn.md) docs. You can use Apache web server using reverse proxy as well.

Following links will guide you how to you a port using Firewalld (in Redhat systems) and Uncomplecated firewall (in Ubuntu systems).


* [Firewalld](https://firewalld.org/documentation/howto/open-a-port-or-service.html)
* [Uncomplicated Firewall](https://www.cyberciti.biz/faq/how-to-open-firewall-port-on-ubuntu-linux-12-04-14-04-lts/)

You can also open a port to one specific IP address for example, an IP of a computing node running a main Nextflow process. Tis more secure than opening a port for all incoming traffics from any source.


