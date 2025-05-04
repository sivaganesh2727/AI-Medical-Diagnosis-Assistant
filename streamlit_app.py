import streamlit as st
import pickle
import pandas as pd
import numpy as np
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re
from interface import render_form

# Load external CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Load the model and data
model = pickle.load(open("model.pkl", "rb"))
severity_df = pd.read_csv("Symptom-severity.csv")
desc_df = pd.read_csv("symptom_Description.csv")
prec_df = pd.read_csv("symptom_precaution.csv")
all_symptoms = severity_df["Symptom"].str.strip().tolist()

# Streamlit App Title
st.title("🩺 AI Medical Diagnosis Assistant")

# User Input Form
with st.form("diagnosis_form"):
    name, email, symptoms_selected, submit = render_form(all_symptoms)

# On form submit
if submit:
    if not symptoms_selected:
        st.warning("⚠️ Please select at least one symptom.")
    else:
        # Input vector generation
        input_vector = [0] * len(all_symptoms)
        for symptom in symptoms_selected:
            if symptom in all_symptoms:
                idx = all_symptoms.index(symptom)
                weight = severity_df.loc[severity_df["Symptom"] == symptom, "weight"].values[0]
                input_vector[idx] = weight

        # Predict disease
        prediction = model.predict([input_vector])[0]

        # Get disease description
        description = desc_df[desc_df["Disease"] == prediction]["Description"].values[0]

        # Get precautions
        precautions = []
        row = prec_df[prec_df["Disease"] == prediction]
        if not row.empty:
            for i in range(1, 5):
                p = row[f"Precaution_{i}"].values[0]
                if pd.notna(p):
                    precautions.append(p)

        # Display result
        st.success(f"🔍 Predicted Disease: **{prediction}**")
        st.info(f"🧾 Description:\n\n{description}")
        if precautions:
            st.warning("💡 Recommended Precautions:")
            for i, p in enumerate(precautions, 1):
                st.write(f"{i}. {p}")

        # Save to database
        try:
            with mysql.connector.connect(
                host="localhost",
                user="root",
                password="siva@222777",  # 🔐 Use your DB password
                database="medical_db"
            ) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO diagnosis (patient_name, symptoms, disease) VALUES (%s, %s, %s)",
                               (name, ", ".join(symptoms_selected), prediction))
                conn.commit()
                st.success("🗂️ Diagnosis saved to database.")
        except Exception as e:
            st.error(f"❌ Database error: {e}")

        # Send diagnosis via email
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            try:
                sender_email = "sivaganeshragam2004@gmail.com"
                sender_password = "psco xeym ckxn yuew"  # 🔑 Use your 16-character Gmail App Password (no spaces)

                # Compose the email
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = email
                message["Subject"] = "Your Medical Diagnosis Report"

                body = f"""Hello {name},

Based on your selected symptoms: {', '.join(symptoms_selected)},
the predicted disease is: {prediction}.

Description:
{description}

Precautions:
{chr(10).join(precautions)}

Stay healthy!
Medical Assistant Team
"""
                message.attach(MIMEText(body, "plain"))

                # Send email
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
                server.quit()

                st.success("📧 Email sent successfully.")
            except smtplib.SMTPAuthenticationError:
                st.error("❌ Email error: Authentication failed. Check your email and app password.")
            except smtplib.SMTPException as e:
                st.error(f"❌ Email error: {e}")
            except Exception as e:
                st.error(f"❌ Unexpected error while sending email: {e}")
        else:
            st.error("❌ Invalid email address. Please enter a valid email.")
