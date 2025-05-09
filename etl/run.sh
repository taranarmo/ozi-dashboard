#!/bin/bash

# Check if job name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <job_yaml_path>"
  exit 1
fi

JOBFILE="$1"

# Run the ETL scheduler with the given job YAML, discard output, and run in background
nohup python3 etl_scheduler.py "$JOBFILE" > /dev/null 2>&1 &