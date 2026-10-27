import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)
DB = OUT / "healthcare_dw.db"

def load_csv(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

if DB.exists():
    DB.unlink()

con = sqlite3.connect(DB)
con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()
cur.executescript("""
CREATE TABLE Dim_Patient (patient_key INTEGER PRIMARY KEY, patient_id INTEGER UNIQUE, patient_name TEXT, gender TEXT, age INTEGER, city TEXT, insurance_plan TEXT);
CREATE TABLE Dim_Doctor (doctor_key INTEGER PRIMARY KEY, doctor_id INTEGER UNIQUE, doctor_name TEXT, specialty TEXT, primary_hospital_id INTEGER);
CREATE TABLE Dim_Hospital (hospital_key INTEGER PRIMARY KEY, hospital_id INTEGER UNIQUE, hospital_name TEXT, city TEXT, state TEXT);
CREATE TABLE Dim_Date (date_key INTEGER PRIMARY KEY, date_id INTEGER UNIQUE, full_date TEXT, year INTEGER, month INTEGER, month_name TEXT, day INTEGER, day_name TEXT, quarter INTEGER);
CREATE TABLE Fact_Patient_Visits (visit_key INTEGER PRIMARY KEY, visit_id INTEGER UNIQUE, patient_key INTEGER, doctor_key INTEGER, hospital_key INTEGER, date_key INTEGER, visit_type TEXT, visit_status TEXT, treatment_cost REAL, length_of_stay_days INTEGER, FOREIGN KEY(patient_key) REFERENCES Dim_Patient(patient_id), FOREIGN KEY(doctor_key) REFERENCES Dim_Doctor(doctor_id), FOREIGN KEY(hospital_key) REFERENCES Dim_Hospital(hospital_id), FOREIGN KEY(date_key) REFERENCES Dim_Date(date_id));
CREATE TABLE Fact_Medication_Records (medication_key INTEGER PRIMARY KEY, medication_id INTEGER UNIQUE, visit_key INTEGER, patient_key INTEGER, doctor_key INTEGER, date_key INTEGER, medication_name TEXT, quantity INTEGER, medication_cost REAL);
""")
def insert(table, cols, rows):
    cur.executemany(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})", rows)

p = load_csv("patients.csv")
d = load_csv("doctors.csv")
h = load_csv("hospitals.csv")
dt = load_csv("dates.csv")
v = load_csv("patient_visits.csv")
m = load_csv("medication_records.csv")
insert("Dim_Patient",["patient_id","patient_name","gender","age","city","insurance_plan"],[(int(x["patient_id"]),x["patient_name"],x["gender"],int(x["age"]),x["city"],x["insurance_plan"]) for x in p])
insert("Dim_Doctor",["doctor_id","doctor_name","specialty","primary_hospital_id"],[(int(x["doctor_id"]),x["doctor_name"],x["specialty"],int(x["primary_hospital_id"])) for x in d])
insert("Dim_Hospital",["hospital_id","hospital_name","city","state"],[(int(x["hospital_id"]),x["hospital_name"],x["city"],x["state"]) for x in h])
insert("Dim_Date",["date_id","full_date","year","month","month_name","day","day_name","quarter"],[(int(x["date_id"]),x["full_date"],int(x["year"]),int(x["month"]),x["month_name"],int(x["day"]),x["day_name"],int(x["quarter"])) for x in dt])
insert("Fact_Patient_Visits",["visit_id","patient_key","doctor_key","hospital_key","date_key","visit_type","visit_status","treatment_cost","length_of_stay_days"],[(int(x["visit_id"]),int(x["patient_id"]),int(x["doctor_id"]),int(x["hospital_id"]),int(x["date_id"]),x["visit_type"],x["visit_status"],float(x["treatment_cost"]),int(x["length_of_stay_days"])) for x in v])
insert("Fact_Medication_Records",["medication_id","visit_key","patient_key","doctor_key","date_key","medication_name","quantity","medication_cost"],[(int(x["medication_id"]),int(x["visit_id"]),int(x["patient_id"]),int(x["doctor_id"]),int(x["date_id"]),x["medication_name"],int(x["quantity"]),float(x["medication_cost"])) for x in m])
con.commit()
queries = {
"SLICE - visits in year 2025": "SELECT d.year, COUNT(*) visits, ROUND(SUM(f.treatment_cost),2) total_cost FROM Fact_Patient_Visits f JOIN Dim_Date d ON f.date_key=d.date_id WHERE d.year=2025 GROUP BY d.year",
"DICE - completed cardiology visits in Andhra Pradesh": "SELECT h.state, doc.specialty, f.visit_status, COUNT(*) visits, ROUND(SUM(f.treatment_cost),2) total_cost FROM Fact_Patient_Visits f JOIN Dim_Hospital h ON f.hospital_key=h.hospital_id JOIN Dim_Doctor doc ON f.doctor_key=doc.doctor_id WHERE h.state='Andhra Pradesh' AND doc.specialty='Cardiology' AND f.visit_status='Completed' GROUP BY h.state,doc.specialty,f.visit_status",
"ROLL-UP - visits by year and quarter": "SELECT d.year,d.quarter,COUNT(*) visits,ROUND(SUM(f.treatment_cost),2) total_cost FROM Fact_Patient_Visits f JOIN Dim_Date d ON f.date_key=d.date_id GROUP BY d.year,d.quarter ORDER BY d.year,d.quarter",
"DRILL-DOWN - visits by month": "SELECT d.year,d.month,d.month_name,COUNT(*) visits FROM Fact_Patient_Visits f JOIN Dim_Date d ON f.date_key=d.date_id GROUP BY d.year,d.month,d.month_name ORDER BY d.year,d.month",
"PIVOT-LIKE - visit type by status": "SELECT visit_type,SUM(CASE WHEN visit_status='Completed' THEN 1 ELSE 0 END) completed,SUM(CASE WHEN visit_status='Scheduled' THEN 1 ELSE 0 END) scheduled,SUM(CASE WHEN visit_status='Cancelled' THEN 1 ELSE 0 END) cancelled FROM Fact_Patient_Visits GROUP BY visit_type ORDER BY visit_type"
}
with open(OUT/"olap_results.txt","w",encoding="utf-8") as f:
    for title,sql in queries.items():
        f.write("\n"+"="*60+"\n"+title+"\n"+"="*60+"\n")
        for row in cur.execute(sql).fetchall(): f.write(str(row)+"\n")
con.close()
print("Healthcare Data Warehouse created successfully.")
print("Patients loaded:",len(p))
print("Doctors loaded:",len(d))
print("Hospitals loaded:",len(h))
print("Dates loaded:",len(dt))
print("Patient visit records loaded:",len(v))
print("Medication records loaded:",len(m))
print("Database:",DB)
print("OLAP results:",OUT/"olap_results.txt")
