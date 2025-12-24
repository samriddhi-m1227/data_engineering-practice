# Postgres + Python SQL Ingestion Pipeline

## Overview
This project implements a **Dockerized data ingestion pipeline** that loads structured CSV data into a **PostgreSQL relational database** using Python and `psycopg2`.  

The pipeline simulates a common analytics workflow: transforming raw CSV files into a normalized relational model suitable for querying and downstream analysis.

---

## Problem
CSV files are commonly used for data exchange but lack structure, constraints, and relational integrity. Loading them directly without modeling can lead to inconsistent data, slow queries, and poor analytics performance.

This project addresses the challenge of:
- Designing a relational schema from raw CSVs
- Enforcing data integrity with keys and constraints
- Efficiently ingesting data into Postgres

---

## Solution
The pipeline performs the following steps:
- Designs relational tables based on CSV structure
- Defines **primary keys**, **foreign keys**, and **indexes**
- Executes DDL statements to create tables in Postgres
- Ingests CSV data using parameterized SQL queries
- Supports safe re-runs via idempotent inserts

---

## 🛠️ Tools & Technologies
- **Python** – ingestion logic and database interaction  
- **PostgreSQL** – relational data storage  
- **psycopg2** – PostgreSQL database adapter for Python  
- **Docker & Docker Compose** – containerized execution  
- **CSV** – structured input data  
- **SQL** – schema definition and constraints  

---

## Database Tables
- **accounts** – customer-level information  
- **products** – product catalog  
- **transactions** – transactional fact table with foreign key relationships  

Indexes are applied to frequently queried columns to support efficient joins and filtering.

---

## How to Run

Build the Docker image:
```bash
docker build -t postgres-python-ingestion .

