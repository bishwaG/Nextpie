

## Example workflow

Nextpie includes an example Nextflow workflow to help users explore its features. This workflow is located in the `assets/example-workflow` directory.

To run the example, refer to the script at:
```
assets/example-workflow/test-runs/run-analysis.sh
```
## Configure Nextflow pipeline for Nextpie 

Nextpie has a client plugin named [nf-nextpie](https://github.com/bishwaG/nf-nextpie). Once you run Nextflow with the command-line option `-plugins nf-nextpie@0.0.1`, Nextflow will automatically download the plugin during runtime and stores it in `$HOME/.nextflow/plugins/nf-nextpie-0.0.1`. This greatly minimizes configuration hassles.
```bash
./nextflow run ../main.nf -plugins nf-nextpie@0.0.1 ....
```
## Plugin configuration

The plugin includes a default configuration file located at `$HOME/.nextflow/plugins/nf-nextpie-0.0.1/classes/nextflow/nextpie/config.json`.

This file defines:

```json
{

"host": "localhost",

"port": 5005,

"api-key": "jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M"

}
```
- host: The hostname or IP address of the machine running Nextpie.

- port: The port Nextpie is running on.

- api-key: The API key used to authenticate with the Nextpie API.

>⚠️ Important: Do not use the default API key in production environments. Always generate a new, secure key for production use.

Once the pipeline run completes, Nextflow's` workflow.complete` event handler will trigger the plugin to upload usage data to Nextpie automatically.

## Firewall configuration

If you have a firewall running in a machine where Nextpie is running, it is essential to open the port on which Nextpie is listening/running. Nextpie runs on port 5000 by default. The port can be changed as required. If you deploy Nextpie into a production setting you could modify the port to 8080 or 80 (this may require root access). Please refer to Gunicorn docs. It is possible to use Apache web server with reverse proxy as well.

The following links will guide you how to open a port using Firewalld (in Redhat systems) and Uncomplecated firewall (in Ubuntu systems). 

* [Firewalld](https://firewalld.org/documentation/howto/open-a-port-or-service.html)
* [Uncomplicated Firewall](https://www.cyberciti.biz/faq/how-to-open-firewall-port-on-ubuntu-linux-12-04-14-04-lts/)

You can also open a port to one specific IP address; for example, an IP of a computing node running a main Nextflow process. This is more secure than opening a port for all incoming traffic from any source.
