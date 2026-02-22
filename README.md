🍺 Brewery BI — End‑to‑End Analytics Project
Python (AI‑assisted) • SQL • DuckDB • Power BI

📌 Overview
Brewery BI is an end‑to‑end analytics project designed to demonstrate practical skills in data engineering, analytics engineering, and business intelligence.
The project simulates a full analytical workflow for a fictional brewery, covering:

data generation (AI‑assisted Python),

SQL transformations and business logic,

multi‑layer data modeling (Bronze → Silver → Gold),

analytical MARTs,

semantic modeling in Power BI,

dashboards for management, sales, production, and logistics.

The goal is to showcase real‑world BI/Data Engineering capabilities in a clean, reproducible, and well‑documented structure.

🧱 Architecture
brewery_bi/
│
├── data/                 # Generated and raw datasets
├── python/               # AI-assisted Python scripts for data generation
├── sql/                  # SQL models: Bronze, Silver, Gold, MARTs
├── duckdb/               # DuckDB database files
├── powerbi/              # .pbix file + screenshots
└── README.md             # Project documentation

AI‑assisted Python → SQL Transformations → DuckDB → Power BI Semantic Model → Dashboards
1. Data Generation (AI‑assisted Python)
Python is used with AI support to generate realistic datasets for:

sales,

production,

logistics,

quality,

customers,

products (beer types),

plants and regions.

The generated data includes realistic patterns such as seasonality, production variability, downtime, waste, and margin behavior.

2. SQL Transformations & Business Logic
All transformations are executed in DuckDB using SQL.

Key components:

Date dimension with full calendar logic

Bronze layer — raw structured data

Silver layer — cleaned and standardized tables

Gold layer — analytical models and MARTs

KPI logic implemented in SQL:

Revenue

Margin

Produced Volume

OEE

Waste

Inventory Coverage

YoY, MoM, rolling metrics

3. DuckDB as the Analytical Engine
DuckDB is used as a lightweight, high‑performance analytical database.

Benefits:

SQL on local files

fast columnar execution

perfect for BI prototyping

easy integration with Power BI

4. Power BI Semantic Model & Dashboards
The Power BI report includes:

Pages
Management — high‑level KPIs (Revenue, Margin, Volume, Inventory Coverage)

Sales & Market — revenue by region, customer, channel, time

Production & Quality — OEE, downtime, waste, defect rate

Logistics — stock levels, inventory coverage, daily sales

Drill‑down / Drill‑through — product‑level and plant‑level details

DAX Highlights
Time intelligence (YoY, MoM, YTD)

KPI logic with CALCULATE + VAR patterns

Rolling windows

Dynamic drill‑through filters

Star Schema semantic model

📂 Repository Structure
Kod
brewery_bi/
│
├── data/                 # Generated and raw datasets
├── python/               # AI-assisted Python scripts for data generation
├── sql/                  # SQL models: Bronze, Silver, Gold, MARTs
├── duckdb/               # DuckDB database files
├── powerbi/              # .pbix file + screenshots
└── README.md             # Project documentation
🧰 Tech Stack
SQL (DuckDB, Firebird SQL, T‑SQL)

Power BI (DAX, semantic modeling, dashboards)

Python (AI‑assisted)

DuckDB

Git / GitHub

ERP experience: Rekord.ERP (Firebird DB), Microsoft Dynamics NAV

🎯 Purpose of the Project
This project was created to demonstrate practical skills required for roles such as:

BI Engineer

Analytics Engineer

Data Engineer (Junior/Mid)

Power BI Developer

It reflects real‑world BI workflows: modeling, SQL transformations, KPI logic, DAX, and dashboard design.

🚧 Work in Progress
The project is actively developed. Upcoming improvements:

automated pipeline (dbt or Python orchestration),

data quality tests,

CI/CD for Power BI and DuckDB,

documentation of SQL models,

extended drill‑through analytics.

📬 Contact
Bartłomiej Lachendrowicz  
📧 bartlomiej.lachendrowicz@gmail.com
🔗 GitHub: github.com/grubyyyyy  (recommended to rename for professional branding)