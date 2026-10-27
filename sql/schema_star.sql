-- Healthcare Data Warehouse: Star / Fact Constellation Schema
PRAGMA foreign_keys = ON;
CREATE TABLE Dim_Patient (patient_key INTEGER PRIMARY KEY, patient_id INTEGER UNIQUE, patient_name TEXT NOT NULL, gender TEXT, age INTEGER, city TEXT, insurance_plan TEXT);
CREATE TABLE Dim_Doctor (doctor_key INTEGER PRIMARY KEY, doctor_id INTEGER UNIQUE, doctor_name TEXT NOT NULL, specialty TEXT, primary_hospital_id INTEGER);
CREATE TABLE Dim_Hospital (hospital_key INTEGER PRIMARY KEY, hospital_id INTEGER UNIQUE, hospital_name TEXT NOT NULL, city TEXT, state TEXT);
CREATE TABLE Dim_Date (date_key INTEGER PRIMARY KEY, date_id INTEGER UNIQUE, full_date TEXT, year INTEGER, month INTEGER, month_name TEXT, day INTEGER, day_name TEXT, quarter INTEGER);
CREATE TABLE Fact_Patient_Visits (visit_key INTEGER PRIMARY KEY, visit_id INTEGER UNIQUE, patient_key INTEGER, doctor_key INTEGER, hospital_key INTEGER, date_key INTEGER, visit_type TEXT, visit_status TEXT, treatment_cost REAL, length_of_stay_days INTEGER, FOREIGN KEY(patient_key) REFERENCES Dim_Patient(patient_key), FOREIGN KEY(doctor_key) REFERENCES Dim_Doctor(doctor_key), FOREIGN KEY(hospital_key) REFERENCES Dim_Hospital(hospital_key), FOREIGN KEY(date_key) REFERENCES Dim_Date(date_key));
CREATE TABLE Fact_Medication_Records (medication_key INTEGER PRIMARY KEY, medication_id INTEGER UNIQUE, visit_key INTEGER, patient_key INTEGER, doctor_key INTEGER, date_key INTEGER, medication_name TEXT, quantity INTEGER, medication_cost REAL);
