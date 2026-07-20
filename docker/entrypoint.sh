#!/usr/bin/env bash
set -e

echo "Starting EchoChain Lakehouse Analytics Container..."
python datasets/generate_datasets.py
python pyspark_pipeline/run_pipeline.py
python scripts/generate_screenshots.py

echo "EchoChain Container Execution Completed Successfully."
exec "$@"
