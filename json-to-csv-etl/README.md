# JSON to CSV ETL Pipeline
## Overview
This project implements a small, **Dockerized Python ETL pipeline** that ingests nested JSON files from a ragged directory structure, flattens semi-structured data, and outputs analytics-ready CSV files.
It simulates a common data engineering task: converting raw JSON data into a tabular format suitable for downstream analytics or database ingestion.
---
## Problem
JSON data is often stored across deeply nested directories and contains nested fields that are not directly usable for analytics. This project addresses that challenge by programmatically discovering, transforming, and normalizing semi-structured data.
---
## Solution
The pipeline performs the following steps:
- Recursively crawls the `data/` directory to identify all JSON files
- Loads each JSON file into Python
- Flattens nested structures into a single-level schema
- Writes one CSV file per JSON file with explicit column headers
---
## How to Run
Build the Docker image:
```bash
docker build -t json-to-csv-etl .
