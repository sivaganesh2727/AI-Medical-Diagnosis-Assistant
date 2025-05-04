# 🩺 AI Medical Diagnosis Assistant

An AI-powered web application built with **Streamlit** that predicts possible diseases based on user-selected symptoms using a machine learning model. It provides detailed descriptions, recommended precautions, and stores results in a **MySQL** database. The app also sends email reports to patients.

---

## 🚀 Features

- 🔍 Predicts disease based on symptoms using trained ML model
- 📋 Describes the disease and gives 4 recommended precautions
- 💾 Stores patient details and diagnosis in a MySQL database
- 📧 Sends diagnosis reports via email to patients
- 🎨 Stylish frontend with custom CSS
- ✅ Secure: Uses `.gitignore` and environment-safe practices

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit, HTML/CSS
- **Backend**: Python (scikit-learn, smtplib, email)
- **Database**: MySQL
- **Machine Learning**: Trained model with symptom severity dataset

---

## 📁 Project Structure

├── app.py # Main Streamlit app
├── interface.py # Handles form inputs
├── model.pkl # Trained machine learning model
├── Symptom-severity.csv # Symptom weight data
├── symptom_Description.csv
├── symptom_precaution.csv
├── style.css # Custom CSS styling
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore rules

## 💻 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-medical-diagnosis-app.git
cd ai-medical-diagnosis-app

Set up Python environment
pip install -r requirements.txt

 Configure your MySQL database
Create a MySQL database and table:

sql
CREATE DATABASE medical_db;
USE medical_db;

CREATE TABLE diagnosis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100),
    symptoms TEXT,
    disease VARCHAR(100)
);
Update your app.py database credentials accordingly.

Generate Gmail App Password
Enable 2-Step Verification on your Gmail.

Generate an App Password from: https://myaccount.google.com/apppasswords

Replace the placeholder in app.py:
python
sender_email = "your_email@gmail.com"
sender_password = "your_16_char_app_password"

Run the App Locally
streamlit run app.py

 Deployment (Streamlit Cloud)
Push your code to GitHub.

Go to Streamlit Cloud

Click "New App" → Choose your repo

Set required secrets:

SENDER_EMAIL

SENDER_PASSWORD

Click "Deploy"

Author
Siva Ganesh Ragam
Connect with me on LinkedIn

License
This project is licensed under the MIT License.
