# ECHO

## Enterprise Consumer Heartbeat and Opinion Network

**Project owner:** Abdur Rahman (Rahven)
**Repository:** https://github.com/rahven-man/ECHO
**Branch:** `main`
**Document status:** Living project brief
**Last updated:** 2026-10-23

---

## 1. Project overview

ECHO is an end-to-end analytics project built on the official Yelp Open Dataset. The project treats Yelp as the source system for a local-business review platform and builds the kind of reporting workflow an analytics team might use in practice.

The raw data is stored as JSON Lines files. It will be loaded into a MySQL staging database, transformed into a warehouse-style star schema, analysed with SQL, and presented through Power BI and Excel. A later version may add a sentiment-analysis layer that compares the language of a review with its star rating.

The project is intentionally focused on analytics engineering and business reporting rather than on building a web application. Its main purpose is to demonstrate practical SQL, ETL, data modelling, BI, and documentation skills in one coherent project.

### What the finished project should demonstrate

- Designing a data flow from raw files to a reporting layer.
- Working with a large dataset without loading entire files into memory.
- Building repeatable Python ETL processes.
- Using MySQL for staging, modelling, validation, and analysis.
- Writing practical SQL with joins, CTEs, window functions, views, and indexes.
- Creating a useful Power BI dashboard and a refreshable Excel report.
- Explaining assumptions and limitations honestly.

---

## 2. Background and learning goals

Rahven is a second-year B.Tech Computer Science student from a tier-3 college in Dehradun, preparing for data analyst and data science roles. He already has experience with Pandas, NumPy, Seaborn, Matplotlib, Scikit-Learn, XGBoost, neural networks, and SQL. He has also completed VENTURI, an end-to-end F1 predictive analytics project.

ECHO fills a different gap. The goal is to gain experience using SQL and relational databases as part of a complete analytics workflow, rather than using a notebook as the entire project. It also provides practice with ETL, warehouse design, Power BI, Excel reporting, project setup, and professional documentation.

The project is being built independently. AI tools may be used as reviewers, explainers, or coding assistants when needed, but the design decisions and core implementation should remain understandable to the owner.

### Learning objectives

1. Use SQL regularly for schema design, cleaning, validation, analysis, views, and optimisation.
2. Understand the separation between raw, staging, warehouse, and serving layers.
3. Build ETL scripts that are streaming, batched, logged, and rerunnable.
4. Learn practical Power BI modelling and DAX.
5. Produce a corporate-style Excel report connected to the data.
6. Document technical choices clearly enough to reproduce the setup later.

---

## 3. Scope and success criteria

### Version 1

Version 1 covers the foundation, staging ETL, warehouse modelling, SQL analysis, Power BI, Excel, and final project packaging. It includes Phases 0 to 4 and Phase 6 in the roadmap.

Version 1 is complete when:

- All five Yelp files have been loaded into MySQL and their row counts reconcile with `docs/data_profile.txt`.
- The ETL process can be rerun safely and has been tested on a small sample first.
- The warehouse schema and its grain statements are documented.
- There are 15 to 20 documented business-question SQL queries.
- There are 5 to 6 reusable SQL views or serving tables.
- Power BI contains Executive, Trends, and Geo pages.
- Excel contains a refreshable connected report.
- The repository includes a clear README, architecture diagram, setup playbook, and one-page case study.

### Version 2

Version 2 starts only after Version 1 is complete. It may include:

- Sentiment scoring for review text.
- Detection of disagreement between sentiment and star rating.
- A `predicted_sentiment_scores` table written back to MySQL.
- Optional forecasting if it adds meaningful value.

### Outside the scope

- Real-time ingestion or streaming production infrastructure.
- Cloud deployment.
- A web application.
- Social-graph analysis using the `friends` field.
- The Yelp photos dataset.
- Revenue, sales, orders, or price analysis, because those fields are not in the source data.

The repository follows a simple scope rule: create a folder or file when its first real content is needed, not in anticipation of future work.

---

## 4. Business context

ECHO represents the analytics layer of a local-business review platform. The platform wants to understand customer opinion, review activity, business performance signals, and patterns in customer visits.

### Intended stakeholders

- **Business owners and branch managers:** rating trends, customer activity patterns, peer comparisons, and warning signs.
- **Platform product and operations managers:** category and city performance, businesses that may need attention, and changes in reviewer behaviour.

### Important limitations of the source

The Yelp dataset contains ratings, reviews, tips, check-ins, user information, and business metadata. It does not contain sales, revenue, orders, or reliable prices. ECHO must therefore describe opinion and activity signals, not financial performance.

Check-ins are also only a proxy for visits. They represent activity recorded by users through the Yelp app, not total foot traffic.

---

## 5. Business questions

These questions define the current analytical direction. They can be refined as the warehouse is designed, but changes should be recorded in the decision log.

| ID | Question | Main data and technique | Version |
|---|---|---|---|
| Q1 | How does a business's average rating change month over month, and how does it compare with its city and category averages? | Reviews, businesses, CTEs, `LAG`, windowed averages | V1 |
| Q2 | At which hours, weekdays, and months are check-ins most common? | Check-ins, businesses, date/time functions | V1 |
| Q3 | How does a business rank against peers in the same city and category? | Businesses, categories, reviews, `RANK`, `DENSE_RANK` | V1 |
| Q4 | Which categories and cities show increasing or decreasing review activity? | Reviews, businesses, time-series comparisons | V1 |
| Q5 | Which businesses may be at risk because their rating or review volume is falling? | Reviews, businesses, rolling windows and thresholds | V1 |
| Q6 | What differs between open and closed businesses? | Businesses and reviews, segmentation | V1 |
| Q7 | How are star ratings distributed, and what relates to useful, funny, and cool votes? | Reviews, distributions, review-length buckets | V1 |
| Q8 | How do elite users differ from non-elite users? | Users and reviews, segmentation | V1 |
| Q9 | How do reviewer cohorts behave over time? | Users and reviews, cohort analysis | V1 |
| Q10 | Which businesses are popular but poorly rated, or well rated but rarely visited? | Check-ins, reviews, quadrant analysis | V1 |
| Q11 | Which cities and states lead in business count, rating, and review volume? | Businesses and reviews, aggregation and maps | V1 |
| Q12 | Where do review sentiment and star rating disagree? | Review text and NLP | V2 |

---

## 6. Data

### Source and handling

The source is the official Yelp Open Dataset. The downloaded `Yelp-JSON.zip` contains `yelp_dataset.tar`, which has been extracted into `data/raw/`.

The files are JSON Lines (NDJSON), not one large JSON array. Each line is one complete JSON object. Raw data must never be edited, committed, or redistributed. Yelp's dataset terms apply. The `data/` directory is ignored by Git, and notebook outputs containing review text or user data must be cleared before committing.

### Current data profile

| File | Rows | Approx. size | One row represents | Important observations |
|---|---:|---:|---|---|
| business | 150,346 | 0.11 GB | One business | Nested `attributes` and `hours`; comma-separated `categories`; 103 null category values; minimum `review_count` is 5 |
| review | 6,990,280 | 4.98 GB | One review | `useful`, `funny`, and `cool` include `-1`; `date` is a string; `text` can be 5,000 characters |
| user | 1,987,897 | 3.13 GB | One user | `friends` can be 359,878 characters and is out of scope; `elite` needs further inspection |
| checkin | 131,930 | 0.27 GB | One business record | `date` contains comma-separated timestamps and must be exploded into check-in rows |
| tip | 908,915 | 0.17 GB | One tip | No single source primary key; `user_id + business_id + date` is effectively unique |

Join keys:

- `business_id`: business, review, checkin, and tip.
- `user_id`: user, review, and tip.

The complete field-level profile is in [`data_profile.txt`](data_profile.txt). Cleaning notes are in [`data_notes.md`](data_notes.md).

### Known limitations

- Every business has at least five reviews because of a limitation of the released dataset. Brand-new businesses are not represented.
- Check-ins are an app-activity proxy, not a complete foot-traffic count.
- The data is a historical snapshot, not a live operational database.

---

## 7. Planned architecture

```text
[Raw JSON Lines files in data/raw/]
              |
              | Phase 1: Python streaming ETL and batch inserts
              v
[MySQL: echo_staging]
  Flattened source mirror with minimal cleaning
              |
              | Phase 2: SQL transformations and modelling
              v
[MySQL: echo_dw]
  Star-schema warehouse
              |
              +--> Serving views and summary tables
              |       +--> Power BI dashboard
              |       +--> Connected Excel report
              |
              +--> Version 2: Python NLP scoring
                      +--> predicted_sentiment_scores in MySQL
```

### Warehouse grain and tables

The following grain statements are the starting point for the warehouse design:

- `fact_review`: one row per review.
- `fact_checkin`: one row per check-in timestamp, exploded from the business-level string.
- `fact_tip`: one row per tip.
- `dim_business`: business details, location, current stars, review count, and open/closed status.
- `dim_user`: user profile fields, with `friends` dropped, plus elite and compliment information.
- `dim_date`: date, year, quarter, month, weekday, and weekend flag.
- `dim_category`: one row per category.
- `bridge_business_category`: many-to-many relationship between businesses and categories.

Still under consideration:

- A key-value `business_attribute` table versus selected columns in `dim_business`.
- A bridge table for elite years.
- A separate `review_text` table versus keeping text in `fact_review`.
- A `dim_time` table for hour-level check-in analysis.

The staging layer should remain close to the source. Business rules and modelling belong in the warehouse. BI tools should read from serving views or summary tables, not directly from raw or staging tables.

---

## 8. Technology and environment

| Area | Current choice |
|---|---|
| Operating system | Windows and PowerShell |
| Editor | VS Code, with Jupyter notebooks through `ipykernel` |
| Python | 3.13.2, virtual environment at `.venv` |
| Main Python packages | pandas, SQLAlchemy, PyMySQL, python-dotenv, tqdm, ipykernel |
| Database | MySQL Server 8.0.45 and MySQL Workbench 8.0 |
| Version control | Git and GitHub |
| BI | Power BI Desktop, planned Import mode |
| Reporting | Excel connected to the database or semantic model |
| Version 2 | Python NLP libraries, to be selected later |

The machine has about 7.6 GB of usable RAM and roughly 318 GB free on the C: drive. Large files such as `review.json` and `user.json` must never be loaded completely into memory. ETL should use generators, batches, and conservative MySQL settings.

### Database conventions

- `echo_staging` is the existing staging database.
- `echo_dw` will be created at the start of Phase 2.
- `echo_user` is the application account and should receive only the permissions it needs.
- `utf8mb4` is required because review text can contain emojis.
- Credentials belong only in `.env`, using `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`.
- `.env` must never be committed or pasted into chat.

---

## 9. Roadmap

| Phase | Focus | Exit condition |
|---|---|---|
| 0. Foundation | Repository, environment, connection, profiling, exploration, brief, schema sketch | Brief and schema sketch are approved |
| 1. ETL to staging | Streaming JSON flattening, batch loading, validation, logging, cleaning | Staging counts match the profile and ETL is rerunnable |
| 2. Warehouse and SQL | Star schema, indexes, views, analytical queries | Warehouse works, with 15 to 20 queries and 5 to 6 views |
| 3. Power BI | Data model, DAX measures, Executive, Trends, and Geo pages | Dashboard refreshes successfully from MySQL |
| 4. Excel | Connected workbook and pivots | Report refreshes successfully |
| 5. ML/NLP, Version 2 | Sentiment discrepancy engine and write-back | Predictions table is populated and documented |
| 6. Packaging | README, diagram, setup playbook, and case study | Repository is ready for a recruiter to review |

The next phase starts only after the previous phase's exit condition is met. From Phase 2 onward, Rahven's preference is to write the SQL and code himself, then use AI for review and explanation rather than copying a complete solution.

---

## 10. Repository structure and working rules

```text
echo/
├── README.md
├── .gitignore
├── requirements.txt
├── docs/
│   ├── project_brief.md
│   ├── data_profile.txt
│   └── data_notes.md
├── data/
│   └── raw/
├── notebooks/
│   └── 01_explore_raw.ipynb
└── src/
    ├── check_connection.py
    └── profile_data.py
```

Ignored local-only items include `.venv/`, `.env`, and `data/`.

1. Add folders only when the first real file for that area is needed.
2. Never edit the raw data.
3. Never commit `.env`, `data/`, or notebook outputs containing Yelp content.
4. Test scripts with a small `--limit` sample before a full run.
5. Make small commits with clear messages and push after each working step.
6. Keep this brief, the README, and the setup playbook aligned with the actual repository.

---

## 11. Current status

**Phase 0 is approximately 90% complete as of 2026-10-23.**

### Completed

- Project plan agreed: Version 1 is the core analytics project; Version 2 is ML/NLP.
- Repository created locally at `C:\Projects\echo` and pushed to GitHub.
- Python 3.13.2 virtual environment and `requirements.txt` created.
- MySQL 8.0.45 configured with `echo_staging` and `echo_user`.
- Python-to-MySQL connection verified.
- Yelp data extracted into `data/raw/` and kept out of version control.
- Full streaming data profile completed in about seven minutes without memory problems.
- Notebook exploration of all five tables completed.
- Findings recorded in [`data_notes.md`](data_notes.md) and [`data_profile.txt`](data_profile.txt).

### Next steps

1. Confirm the business questions, scope, and this brief.
2. Draft and review the warehouse schema, including grain statements.
3. Mark Phase 0 complete.
4. Begin Phase 1 by designing staging tables, checking MySQL bulk-load settings, and writing the ETL scripts one at a time.

### Findings worth carrying forward

- All five source files are JSON Lines.
- Full-file profiling found `-1` vote values that did not appear in the 100,000-row sample.
- Nulls were found in `business.attributes`, `business.categories`, and `business.hours`.
- Category strings contain whitespace duplicates and must be stripped before splitting.
- Restaurants account for roughly one-third of businesses.

---

## 12. Risks and constraints

- **Scope creep:** finish Version 1 before starting Version 2.
- **Memory:** stream and batch large files; do not rely on full-file DataFrames.
- **Power BI performance:** use Import mode and aggregated serving views instead of DirectQuery over millions of rows.
- **Data interpretation:** do not present review activity or check-ins as revenue or total visits.
- **Licensing:** keep Yelp data out of GitHub and notebook outputs.
- **Learning quality:** understand copied commands and record setup decisions in the playbook.

---

## 13. Decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-10 | Project name: ECHO | Owner's choice |
| 2026-10 | Use the raw Yelp JSON dataset rather than a flat CSV | Provides realistic scale and requires streaming ETL |
| 2026-10 | Use staging, warehouse, and serving layers | Keeps source data, business logic, and reporting separate |
| 2026-10 | Read JSON Lines line by line | NDJSON is simple to parse without loading the full file |
| 2026-10 | Drop `friends` | Social-graph analysis is out of scope and the field is extremely large |
| 2026-10 | Use a category bridge table | Categories have a many-to-many relationship with businesses |
| 2026-10 | Use Power BI Import mode over views | Avoids the expected performance cost of DirectQuery |
| 2026-10 | Move NLP to Version 2 | Keeps the core SQL and reporting work focused |
| 2026-10 | Use a separate staging database and least-privilege user | Improves layer separation and security hygiene |
| 2026-10 | Create folders only when needed | Avoids unused project structure |

---

## 14. Open decisions

- Store business `attributes` as selected columns or a key-value table.
- Use natural keys, surrogate keys, or a combination in the warehouse.
- Keep review text in `fact_review` or move it to a separate table.
- Treat `-1` in `useful`, `funny`, and `cool` as zero, null, or excluded values.
- Choose between SQLAlchemy batch inserts and `LOAD DATA LOCAL INFILE`.
- Set conservative MySQL bulk-load and memory parameters.
- Choose the date range and granularity of `dim_date`, and decide whether `dim_time` is needed.
- Finalise the business-question list after the schema is clearer.

---

## 15. Maintaining this brief

This document should describe the project as it actually exists, not as it was originally planned. After a meaningful change, update the relevant status, architecture, repository structure, decision log, open decisions, or next steps.

When updating it:

1. Preserve completed work and mark new work as planned or in progress.
2. Replace estimates and assumptions when implementation produces verified facts.
3. Add decisions with their date and reason instead of silently rewriting history.
4. Update row counts or tool versions only when they have been checked.
5. Keep the document useful to both a recruiter reading the project and a developer or AI agent continuing the work.

---

## 16. Glossary

- **Grain:** what one row in a table represents.
- **JSON Lines / NDJSON:** a file format where each line is a separate JSON object.
- **Generator:** a Python function using `yield` to produce one item at a time.
- **ETL:** extract, transform, and load.
- **Staging:** a landing area that stays close to the source format.
- **Star schema:** fact tables connected to descriptive dimension tables.
- **Bridge table:** a table that resolves a many-to-many relationship.
- **Least privilege:** granting an account only the permissions it needs.
- **Serving layer:** views or tables shaped for reporting and analysis.
- **Write-back:** storing model predictions or other derived results in the database.
