# Self-Service Analytics Platform
*dbt + Airflow + LLM-powered natural language queries*

## What This Demonstrates
Prototype of self-service analytics platform enabling Finance and business stakeholders and non-tech PMs to generate ad hoc reports via plain-English queries.

## �Architecture

flowchart TB
  subgraph Ingestion
    A[Raw Data\n(CSV files)] --> B[dbt Project\nstaging + marts]
  end

  subgraph Storage
    C[(DuckDB\nLocal Analytical DB)]
  end

  subgraph Orchestration
    O[Airflow\nScheduled dbt runs] --> B
  end

  subgraph Serving
    S[Streamlit UI\nAd-hoc Request] --> L[LLM Query Layer\nNL → SQL\nSchema-aware + guarded]
    L --> C
    C --> X[Excel Report Generator\nTables + Basic Insights]
  end

  B --> C
  X --> OUT[Stakeholder Output\nExcel (.xlsx)]

## Data Model


## Features
- Natural language to SQL queries
- Automated dbt pipeline orchestration
- Excel/CSV export
- Brazilian e-commerce dataset (100k orders)

## Tech Stack
- dbt (data transformation)
- DuckDB (analytical database)
- Airflow (orchestration)
- Streamlit (UI)
- Claude API (LLM)
- Python, SQL
