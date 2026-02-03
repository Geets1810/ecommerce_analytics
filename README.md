# Overview

Business stakeholders often need ad-hoc reports with little to no advance notice. In many organizations, this creates constant interruptions for analytics teams, slowing down BAU work and introducing inconsistencies in reported numbers.
This project demonstrates a self-service analytics platform that allows stakeholders to query governed data in plain English and receive Excel reports — without direct analyst involvement.
The goal is not to replace analysts, but to reduce low-value ad-hoc work while preserving trust, consistency, and auditability in reporting.

# Problem Statement
Common challenges in analytics teams:
Ad-hoc reporting requests arrive unexpectedly and frequently
Analysts rewrite similar SQL repeatedly
Stakeholders query raw tables, leading to inconsistent metrics
Excel remains the preferred output format despite modern BI tools
# This project addresses those challenges by:
Centralizing logic in dbt-modeled data marts
Providing a controlled natural-language interface for queries
Delivering results in Excel — the format stakeholders already use

# Solution Architecture
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
# Key Features
# Governed Data Models
dbt models define canonical business logic and metrics
Prevents querying raw, inconsistent tables
# Local Analytical Engine
DuckDB used as a fast, modern analytical database
Ideal for reproducible local development and prototyping

# Natural Language Querying
LLM translates plain-English questions into schema-aware SQL
Guardrails restrict queries to approved marts only
# Excel-First Output
Reports generated as .xlsx files
Matches real-world stakeholder workflows

# Orchestration
Airflow schedules dbt refreshes
Separates data freshness from user requests

# Example Workflow
Stakeholder asks:
“Show daily revenue by product category for last month”

# System flow:
Request submitted via Streamlit UI
LLM converts request → validated SQL
SQL runs against dbt-governed DuckDB marts
Results exported to Excel
Stakeholder downloads report

# Technology Stack
Layer	Tools
Data Modeling	dbt
Analytical DB	DuckDB
Orchestration	Airflow
UI	Streamlit
LLM Interface	Anthropic Claude API
Output	Excel (.xlsx)
Language	Python, SQL
Design Decisions & Trade-offs

# DuckDB (Local)

✅ Fast, modern, reproducible
❌ Not designed for multi-user concurrency or large-scale production

# Excel Output

✅ Matches how stakeholders actually consume data
❌ Less interactive than dashboards

# LLM as Interface (Not Logic)

LLM only generates SQL
Business logic remains in dbt models

# No Dashboards by Design
This tool focuses on ad-hoc reporting, not KPI monitoring

# MVP Scope (Intentional)
This project intentionally limits scope to:
One subject area
Governed read-only queries
Batch-refreshed data
Single-user execution

# Future extensions (out of scope here):
Data reconciliation engine
Query auditing & usage analytics
Role-based access control
Multi-warehouse support

# Why This Project

This project reflects real problems faced by analytics teams, not theoretical exercises. It demonstrates:
Analytics engineering fundamentals (dbt, metrics, governance)
Data engineering thinking (orchestration, separation of concerns)
Practical use of LLMs as productivity tools
Stakeholder empathy (Excel, self-serve access)

# My Role

This is a solo, end-to-end project, including:
Data modeling and transformations
Architecture and orchestration design
LLM prompt design and guardrails
UI and reporting layer
Documentation and trade-off analysis

How to Run (Local)
git clone https://github.com/Geets1810/ecommerce_analytics
cd ecommerce_analytics
docker compose up -d
streamlit run app.py

Closing Note
This project is designed as a portfolio demonstration, simulating how modern analytics teams can reduce ad-hoc workload while maintaining trust in reported numbers.
