import pandas as pd
import mysql.connector
import os

# MySQL connection setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",   # Your MySQL username
    password="",   # Your MySQL password
    database="medical_db"  # Replace with your database name
)
cursor = conn.cursor()

# Path to the data folder
data_folder = os.path.join(os.path.dirname(__file__), 'data')

# 1. Insert data into the `symptoms` table
df_symptoms = pd.read_csv(os.path.join(data_folder, "Symptom-severity.csv"))
for index, row in df_symptoms.iterrows():
    cursor.execute("INSERT INTO symptoms (symptom, weight) VALUES (%s, %s)",
                   (row['Symptom'], row['weight']))
conn.commit()

# 2. Insert data into the `diseases` table
df_diseases = pd.read_csv(os.path.join(data_folder, "dataset.csv"))
for index, row in df_diseases.iterrows():
    cursor.execute(""" 
        INSERT INTO diseases (disease, symptom_1, symptom_2, symptom_3, symptom_4, symptom_5, 
                              symptom_6, symptom_7, symptom_8, symptom_9, symptom_10, symptom_11, 
                              symptom_12, symptom_13, symptom_14, symptom_15, symptom_16, symptom_17)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))
conn.commit()

# 3. Insert data into the `disease_description` table
df_desc = pd.read_csv(os.path.join(data_folder, "symptom_Description.csv"))
for index, row in df_desc.iterrows():
    cursor.execute("INSERT INTO disease_description (disease, description) VALUES (%s, %s)",
                   (row['Disease'], row['Description']))
conn.commit()

# 4. Insert data into the `disease_precautions` table
df_precautions = pd.read_csv(os.path.join(data_folder, "symptom_precaution.csv"))
for index, row in df_precautions.iterrows():
    cursor.execute("""
        INSERT INTO disease_precautions (disease, precaution_1, precaution_2, precaution_3, precaution_4)
        VALUES (%s, %s, %s, %s, %s)
    """, tuple(row))
conn.commit()

# 5. Insert a sample diagnosis record into the `diagnosis` table (for testing)
# Modify the values based on your needs or get them from a form/input
patient_name = "John Doe"
symptoms = "Fever, Cough"
disease = "Flu"
email = "john.doe@example.com"
cursor.execute("""
    INSERT INTO diagnosis (patient_name, email, symptoms, disease) 
    VALUES (%s, %s, %s, %s)
""", (patient_name, email, symptoms, disease))
conn.commit()

# Close connection
conn.close()

print("Data inserted successfully!")
