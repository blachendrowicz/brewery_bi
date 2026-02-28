🍺 Brewery BI — End-to-End Analytics Engineering Project

Python (AI-assisted) • SQL • DuckDB • Power BI

📌 Overview

Brewery BI is an end-to-end analytics engineering project that simulates a realistic BI environment for a fictional brewery.

The project demonstrates practical, production-oriented skills across:

Data engineering

Analytics engineering

BI modeling

KPI design and DAX logic

It covers the full lifecycle of data:

Synthetic data generation → SQL transformations → Analytical modeling → Semantic layer → Executive dashboards

The goal is to present a clean, reproducible example of a modern BI workflow built with lightweight, scalable tools.

🏗 Architecture

The repository is structured into clear functional layers:

brewery_bi/
│
├── README.md
│
├── database/
│   └── brewery.duckdb
│
├── generator/
│   ├── main.py
│   ├── create_dimdate_view.py
│   ├── create_mart_monthly.py
│   │
│   └── sql/
│       ├── create_dimdate_view.sql
│       └── mart_margin_month.sql
│
├── power bi/
│   └── Brewery_report.pbix
│
└── screenshots/
Layer Responsibilities

generator/
Python-based synthetic data generator with AI-assisted logic.

database/
DuckDB analytical database serving as the transformation engine.

generator/sql/
SQL logic for building dimensions and analytical marts.

power bi/
Semantic model and dashboard implementation.

screenshots/
Portfolio visuals of final dashboards.

🧪 Data Generation (Python + AI)

Synthetic operational data is generated using Python scripts enhanced with AI-assisted behavioral modeling.

The generator simulates realistic brewery operations across:

Sales

Production

Logistics

Quality

Customers

Products (beer types)

Plants and regions

The dataset includes:

Seasonality patterns

Production variability

Downtime events

Waste and defect behavior

Margin fluctuations

Inventory dynamics

The objective is to produce data that behaves like real operational systems rather than random mock data.

🛠 SQL Transformations & Modeling

All transformations are executed in DuckDB using SQL.

The project follows a layered modeling approach:

Date dimension creation

Standardized Silver-layer tables

Gold-layer analytical models

Monthly KPI marts

Business logic implemented in SQL includes:

Revenue and gross margin calculations

Production volume metrics

OEE computation

Waste and defect rate

Inventory coverage (days)

YoY, MoM, and rolling metrics

The structure mirrors modern analytics engineering practices used in production BI systems.

⚡ DuckDB as Analytical Engine

DuckDB acts as the central transformation engine.

Why DuckDB:

High-performance columnar execution

Lightweight and file-based

No server setup required

Seamless integration with Power BI

Ideal for analytics prototyping

It provides a practical example of local-first analytics architecture.

📊 Power BI Semantic Model & Dashboards

The Power BI report is built on a star-schema semantic model.

Dashboard Pages

Executive Overview
Revenue, Margin, Volume, Inventory Coverage KPIs

Sales & Market
Performance by region, customer, channel, and time

Production & Quality
OEE, downtime, waste, defect rate

Logistics
Stock levels, inventory coverage, daily sales trends

Beer Performance (Drill-through)
Product-level analysis with dynamic filtering

🧮 DAX Highlights

Time intelligence (YoY, MoM, YTD)

Rolling window calculations

KPI delta logic using VAR patterns

Conditional formatting measures

Dynamic drill-through context handling

Clean star-schema optimization

The model separates business logic from visuals and follows performance-oriented DAX patterns.

🧰 Tech Stack

SQL (DuckDB, T-SQL)

Power BI (DAX, semantic modeling, dashboard design)

Python (data generation & orchestration)

DuckDB

Git / GitHub

🎯 Purpose

This project demonstrates job-ready skills relevant to roles such as:

BI Engineer

Analytics Engineer

Data Engineer

Power BI Developer

It reflects real-world BI workflows:

Data modeling

SQL transformations

KPI design

Time intelligence logic

Drill-through analytics

Executive dashboard development

🚧 Roadmap / Improvements

Planned enhancements:

dbt-based transformation layer

Data quality testing

Automated orchestration pipeline

CI/CD for Power BI artifacts

Extended SQL model documentation

Predictive and scenario-based analytics

📬 Contact

Bartłomiej Lachendrowicz
📧 bartlomiej.lachendrowicz@gmail.com

🔗 GitHub: github.com/blachendrowicz