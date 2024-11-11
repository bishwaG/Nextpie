#!/usr/bin/env nextflow
/*
vim: syntax=groovy
-*- mode: groovy;-*-
================================================================================

               E X A M P L E    P I P E L I N E
               
================================================================================
*/

// Pipeline name
pipelineName = "Test-pipeline"

// Enable DSL2
nextflow.enable.dsl=2


def helpMessage() {
    log.info"""
===============================================================================
""" + params.workflow_name + """ v${params.workflow_ver}
===============================================================================

This is an example Nextflow workflow showing how to integrate Nextpie into a 
Nextflow workflow. The workflow takes FAST pairs as input and runs FASTQC and
MultiQC.

Usage:

/path/to/workflow/main.nf --fastqs '*_R{1,2}*.fastq.gz'

Mandatory arguments:

	--fastq		Intput FASTQ pairs. [Default: 'fastq/*_R{1,2}_*.fastq.gz' ]
	--name		Run (or project) name.
	--group		Research group name.
	--outDir	Output direcotry. [Default: results]


""".stripIndent()
}


//-----------------------------------------------------------------------------
// HELP MESSAGE
//-----------------------------------------------------------------------------
params.help = false
if (params.help){
    helpMessage()
    exit 0
}


/******************************************************************************
 * Configurable variables
 ******************************************************************************
 */
params.name             = false
params.group            = false
params.fastqs           = "fastq/*_R{1,2}_*.fastq.gz"
//params.outDir           = "./results"




custom_runName = params.name
if( !(workflow.runName ==~ /[a-z]+_[a-z]+/) ){
  custom_runName = workflow.runName
}

/******************************************************************************
 * Create a channel from input FASTQ pairs
 ******************************************************************************
 */

Channel
    .fromFilePairs( params.fastqs )
    .ifEmpty { exit 1, "ERROR: unable to find FASTQ files matching: ${params.fastqs}" }
    .set { fastq_files }



/******************************************************************************
 * CONFIG HEADER
 ******************************************************************************
 */
log.info "==============================================================================="
log.info " ${params.workflow_name} v${params.workflow_ver}"
log.info "==============================================================================="
def summary = [:]
summary['Run Name']       = custom_runName ?: workflow.runName
summary['Group']          = params.group
summary['FASTQs']         = params.fastqs
summary['Output Dir']     = params.outDir

log.info summary.collect { k,v -> "${k.padRight(15)}: $v" }.join("\n")
log.info "==============================================================================="


// Nextflow version check
include {version_check} from './lib/functions'
version_check(params.nf_required_version, workflow.nextflow.version)

// prompt
include {prompt} from './lib/functions'
prompt(System.console().readLine 'Do you want to continue (y/n)?')


/******************************************************************************
 * RUN WORKFLOW
 ******************************************************************************
 */

// load sub-workflow
include {preprocess}     from './lib/preprocess'

workflow{
	
	// run sub-workflow preprocess
	preprocess(fastq_files)

}


/******************************************************************************
 * ON WORKFLOW COMPLETE
 ******************************************************************************
 */
 
// include Nextpie function
include {Nextpie} from './lib/functions'

workflow.onComplete {
    
	// Nextpie
	// params are defined in nextflow.config
	if(params.nextpie_enable){
	
		log.info "workflow: " + params.workflow_name
		log.info "version : " + params.workflow_ver
		log.info "group   : " + params.group
		log.info "project : " + custom_runName
		
		if(params.name && params.group){		
			log.info "Pushing run metadata to Nextpie http://${params.nextpie_host}:${params.nextpie_port}"
			log.info "Response: " + 
			Nextpie(host      = params.nextpie_host, 
				port      = params.nextpie_port,
				traceFile = "${params.outDir}/pipeline_info/Trace.txt", 
				Workflow  = params.workflow_name, 
				Version   = params.workflow_ver, 
				Group     = params.group, 
				Project   = custom_runName,
				APIkey    = params.nextpie_api_key).toString()
		}else{
			log.info "Run metadata pushing to Nextflow skipped (no --group --name provided)."
			}
		}
}
