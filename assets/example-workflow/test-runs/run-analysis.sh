#!/bin/bash

## limit heap size for nextflow
NXF_OPTS='-Xms1g -Xmx1g'
_JAVA_OPTIONS='-Xms1g -Xmx4g'

export NXF_PLUGINS_TEST_REPOSITORY=https://github.com/bishwaG/nf-nextpie/releases/download/0.0.2/nf-nextpie-0.0.2-meta.json

./nextflow run ../main.nf -plugins nf-nextpie@0.0.2 \
  --fastqs 'fastq/*_R{1,2}*.fastq.gz' \
  --name "test_project" \
  --group "test_research_group"


