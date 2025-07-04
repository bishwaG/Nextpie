


## Example workflow

Nextpie includes an example Nextflow workflow to help users explore its features. This workflow is located in the `assets/example-workflow` directory.

To run the example, refer to the script at:
```
assets/example-workflow/test-runs/run-analysis.sh
```

 
## The Configuration File


Upon first use in a Nextflow pipeline (e.g., using `-plugins nf-nextpie@0.0.2`), the plugin is automatically downloaded to:

```bash
$HOME/.nextflow/plugins/nf-nextpie-0.0.2

```
Its configuration file can be found at:

```bash
$HOME/.nextflow/plugins/nf-nextpie-0.0.2/classes/nextflow/nextpie/config.json
```


The default contents of `config.json` are:

```json
{
  "host": "localhost",
  "port": 5000,
  "api-key": "jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M",
  "workflow-name-var": "workflow_name",
  "workflow-version-var": "workflow_ver"
}
```

### `host`

The hostname or IP address of the machine running the Nextpie server. The default is `localhost`, which refers to the local machine.

### `port`

The port on which the Nextpie server is running. Do not change this unless you know what you're doing or if the default port is already in use.

### `api-key`

An API key required for authentication. The client (`nf-nextpie`) uses this key to authenticate with the Nextpie server. In a production environment, it is highly recommended to generate a unique API key using the Nextpie GUI and replace the default value for security purposes.

> ⚠️ Important: Do not use the default API key in production environments. Always generate a new key for production use.

### `workflow-name-var` and `workflow-version-var`

> ⚠️ NOTE: Do not modify the `workflow-name-var` and `workflow-version-var` variables. These are not user-configurable parameters.


These are the names of the Nextflow variables that store the pipeline name and version, respectively. Their values are expected to be set to `workflow_name` and `workflow_ver`, meaning these variables must exist within your pipeline's `params` scope (e.g., in `nextflow.config`).

The plugin searches for these variables in the `params` scope. Therefore, `workflow_name` and `workflow_ver` should be defined as follows:

```groovy
params {
  workflow_name = 'my-workflow'
  workflow_ver  = '1.0.1'
}
```


The plugin looks for `name` and `version` in the `manifest` scope, and for `workflow_name` and `workflow_ver` in the `params` scope. If `name` and `version` are present in `manifest`, the plugin will **ignore** `workflow_name` and `workflow_ver` from `params` and instead use the values from `manifest`.

If you're using [nf-schema](https://github.com/nextflow-io/nf-schema) in your pipeline, leveraging the `manifest` scope is often more advantageous, as it avoids the need for intrusive modifications to your Nextflow pipeline. As long as the `name` and `version` variables are defined in the `manifest` scope, they will be automatically picked up by the plugin.

While `nf-nextpie` can retrieve the workflow name and version from the `params` scope, using the `manifest` scope is highly recommended. It is considered best practice to store pipeline metadata—such as `name`, `version`, `affiliation`, `email`, `github`, and similar fields—within the `manifest` block.
**Example:**

```groovy
manifest {
  name    = 'my-workflow'
  version = '1.0.1'
}
```
> NOTE: Both `params` and `manifest` scopes are defined in the Nextflow pipeline's configuration file (`nextflow.config`).
> 
## Integrating `nf-nextpie` with a Nextflow Pipeline

There are two ways to integrate `nf-nextpie` into a Nextflow pipeline:

### ✅ Option 1: Using `nextflow.config`

Add the following to the `plugins` block in `nextflow.config`:

```groovy
plugins {
  id 'nf-nextpie@0.0.2'
}
```

This allows all runs of the pipeline to use the plugin by default.

### ✅ Option 2: Using the Command Line

Supply the plugin using the command-line option for each run:

```bash
nextflow run mypipeline.nf -plugins nf-nextpie@0.0.2
```

## Firewall configuration

If you have a firewall running in a machine where Nextpie is running, it is essential to open the port on which Nextpie is listening/running. Nextpie runs on port 5000 by default. The port can be changed as required. If you deploy Nextpie into a production setting you could modify the port to 8080 or 80 (this may require root access). Please refer to Gunicorn docs. It is possible to use Apache web server with reverse proxy as well.

The following links will guide you how to open a port using Firewalld (in Redhat systems) and Uncomplecated firewall (in Ubuntu systems). 

* [Firewalld](https://firewalld.org/documentation/howto/open-a-port-or-service.html)
* [Uncomplicated Firewall](https://www.cyberciti.biz/faq/how-to-open-firewall-port-on-ubuntu-linux-12-04-14-04-lts/)

You can also open a port to one specific IP address; for example, an IP of a computing node running a main Nextflow process. This is more secure than opening a port for all incoming traffic from any source.
