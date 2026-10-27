# Healthcare Data Warehouse Project

A runnable beginner project for a Data Warehouse lab using Python's built-in SQLite support.
All records are synthetic/fictitious.

## Contents
- `data/patients.csv` — 150 patient dimension records
- `data/doctors.csv` — 15 doctor dimension records
- `data/hospitals.csv` — 5 hospital dimension records
- `data/dates.csv` — 365 calendar records for 2025
- `data/patient_visits.csv` — exactly 500 patient visit input records
- `data/medication_records.csv` — 300 medication records
- `sql/schema_star.sql` — Star/Fact Constellation table definitions
- `sql/schema_snowflake.sql` — example normalized hospital/location dimension
- `sql/schema_constellation.sql` — explanation of shared fact constellation
- `scripts/build_warehouse.py` — creates database, loads CSVs and runs OLAP queries
- `output/` — generated database and OLAP results appear here after running

## Run in VS Code (Windows)
1. In VS Code choose File → Open Folder and select `HealthcareDW_Project`.
2. Open Terminal → New Terminal.
3. Run `python --version` (or `py --version`) to check Python.
4. Run `python scripts/build_warehouse.py`. If that command is unavailable, try `py scripts/build_warehouse.py`.
5. Look in `output/` for `healthcare_dw.db` and `olap_results.txt`.

No pip install and no internet connection are required. Python's standard library is enough.

## OLAP examples
- Slice: visits for year 2025
- Dice: completed cardiology visits in Andhra Pradesh
- Roll-up: group by year and quarter
- Drill-down: group by month
- Pivot-like: visit type compared across status columns

## Schema note
The runnable database contains a star-style dimensional model with two fact tables sharing dimensions, demonstrating a Fact Constellation. The Snowflake SQL file illustrates normalization of hospital location; it is a teaching snippet and is not automatically run by the build script. If your lab specifically requires Pentaho Data Integration, the CSV files can be used as input sources in Pentaho.
