-- Snowflake Schema: Hospital location is normalized into a separate dimension
CREATE TABLE Dim_Location (location_key INTEGER PRIMARY KEY, city TEXT NOT NULL, state TEXT NOT NULL, UNIQUE(city,state));
CREATE TABLE Dim_Hospital (hospital_key INTEGER PRIMARY KEY, hospital_id INTEGER UNIQUE, hospital_name TEXT NOT NULL, location_key INTEGER, FOREIGN KEY(location_key) REFERENCES Dim_Location(location_key));
-- Dim_Patient, Dim_Doctor, Dim_Date and Fact_Patient_Visits are similar to schema_star.sql
