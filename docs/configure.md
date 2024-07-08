## An Example workflow

Nextflow comes with an example Nextflow workflow to help integrate Nextpie to any Nextflow workflow. The example workflow is located in `example-workflow` directory. 

## Configure Nextflow pipeline for Nextpie

Nextpie contains contains a function `Nextpie` which is defined in the file `example-workflow/lib/functions.nf`. The function has following arguments/parameters.

```
Nextpie(host      = NEXTPIE_HOST_IP_ADDRESS, 
	port      = NEXTPIE_PORT,
	traceFile = "PATH_TO_Trace.txt", 
	Workflow  = WORFLOW_NAME, 
	Version   = WORKFLOW_VERSION, 
	Group     = RESEARCH_GROUP, 
	Project   = RUN_NAME or PROEJCT_NAME,
	APIkey    = NEXTPIE_API_KEY)
```

Descriptions:
| Arguments|Details  |
|-----------|-----------------------------------------------------------------|
| host      | An IP address of a machine that has Nextpie running             |
| port      | A port number on which Nextpie is running (degault: 5000)       |
| traceFile | Path to trace.txt/Trace.txt produced by a Nextflow workflow     |
| Workflow  | Workflow name                                                   |
| Version   | Workflow version                                                |
| Group     | Name of a research group                                        |
| Project   | Name of a research project or a Nextflow run name               |
| APIkey    | API key produced from Nextpie GUI (setting page). A user should have an API access to be able to use the key. The access can be given from [admin page](admin.md).

To use the function `Nextpie()` inside Nextflow's `workflow.onComplete`. In the example workflow Nextflow parameters (`nextpie_host`, `nextpie_port`, `workflow_name`, `workflow_ver`, `nextpie_api_key`) are defined to pass to Nextpie's fixed parameters (`host`, `port`, `Workflow`, `Version` and `APIkey`) in `example-workflow/nextflow.config` as shown below. Non fixed parameters such as `traceFile`, `Group` and `Project` are taken from Nextflow's commanline input using flags `--group` and `project`.

```groovy
params {
	//Pipeline name and version
	workflow_name = 'Test-workflow'
	workflow_ver  = '0.0.1' 
	
	// Nextpie config
	nextpie_host    = "localhost"
	nextpie_port    = 5000
	nextpie_api_key = "uDS06L5qRof86CMF3KtOCeWsKTxkpw"
	nextpie_enable  = true
}
```

Following code from `example-workflow/main.nf` shows an usage example of Nextpie function. The function will throw exceptions in case it can reach Nextpie server or encounters erros in Nextpie.
```groovy
// include Nextpie function
include {Nextpie} from './lib/functions'

workflow.onComplete {
    
	// Nextpie
	// params.nextpie_enable defined in nextflow.config
	if(params.nextpie_enable){
	
		// Logging
		// params.workflow_name and params.workflow_ver come from nextflow.config.
		// Refer above code block
		log.info "workflow: " + params.workflow_name
		log.info "version : " + params.workflow_ver
		// params.group is taken from commandline using --group flag
		log.info "group   : " + params.group
		log.info "project : " + workflow.runName
		
		// Push run metadata when group and name is provided
		if(params.name && params.group){		
			log.info "Pushing metadata to Nextpie http://${params.nextpie_host}:${params.nextpie_port}"
			log.info "Response: " + 
			Nextpie(host      = params.nextpie_host, 
				port      = params.nextpie_port,
				traceFile = "${params.outDir}/pipeline_info/Trace.txt", 
				Workflow  = params.workflow_name, 
				Version   = params.workflow_ver, 
				Group     = params.group, 
				Project   = workflow.runName,
				APIkey    = params.nextpie_api_key).toString()
		}else{
			log.info "Run metadata pushing to Nextflow skipped (no --group --name provided)."
			}
		}
}
```

## Firewall configuration

If you have a firewall running in a machine where is Nextpie is running, it is essential to open Nextpie port. Nextpie run by default on port `5000` on development mode. On production mode it runs on port `8001` using [Gunicorn](deploy-prod.md) or []Gunicorn](deploy-prod.md) by default. The port can be changed according to your need. It can also be configured to ih Apache web server using reverse proxy.

Following links will guide you how to you a port using Firewalld (in Redhat systems) and Uncomplecated firewall (in Ubuntu systems).


* [Firewalld](https://firewalld.org/documentation/howto/open-a-port-or-service.html)
* [Uncomplicated Firewall](https://www.cyberciti.biz/faq/how-to-open-firewall-port-on-ubuntu-linux-12-04-14-04-lts/)

You can also open a port to one specific IP address for example, an IP of a computing node running a main Nextflow process. Tis more secure than opening a port for all incoming traffics from any source.


