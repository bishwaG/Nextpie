#!/bin/bash

## limit heap size for nextflow
NXF_OPTS='-Xms1g -Xmx1g'
_JAVA_OPTIONS='-Xms1g -Xmx4g'


./nextflow run ../main.nf -plugins nf-nextpie@0.0.1 \
  --fastqs 'fastq/*_R{1,2}*.fastq.gz' \
  --name "test_project" \
  --group "test_research_group"


