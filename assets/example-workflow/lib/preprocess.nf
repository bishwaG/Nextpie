#!/usr/bin/env nextflow
/*
vim: syntax=groovy
-*- mode: groovy;-*-
================================================================================
               NEXTFLOW EXAMPLE WORKFLOW
================================================================================
*/


/*
*******************************************************************************
* STEP 1 - FastQC
*******************************************************************************
 */
process FastQC {
    tag "$prefix"
    publishDir "${params.outDir}/FastQC", mode: 'copy',
        saveAs: {filename -> filename.indexOf(".zip") > 0 ? "zips/$filename" : "$filename"}

    input:
    tuple val(fastq), path(fastq_pair)

    output:
    path "*_fastqc.{zip,html}", emit: fastqc_report

    script:
    prefix = fastq_pair[0].toString() - ~/(_S[0-9]{1,3}_L[0-8]{3}_R1_001)?(_S[0-9]{1,3}_R1_001)?(\.fq)?(\.fastq)?(\.gz)?$/
    
    """
    fastqc --threads ${task.cpus} $fastq_pair
    """
}


workflow preprocess
{
	take:
	fastq
	
	main:
	FastQC(fastq)
		

	emit:
	fastqc_report = FastQC.out.fastqc_report
	
}
 
