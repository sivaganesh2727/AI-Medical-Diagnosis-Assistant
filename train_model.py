import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load datasets
df = pd.read_csv("dataset.csv")
severity_df = pd.read_csv("Symptom-severity.csv")

# Prepare list of all symptoms (cleaned)
all_symptoms = severity_df["Symptom"].str.strip().tolist()

# Replace NaNs with 'None'
df.fillna("None", inplace=True)

# Create encoded dataset
X = []
for _, row in df.iterrows():
    symptom_vector = [0] * len(all_symptoms)
    for col in row.index[1:]:  # Skip 'Disease'
        symptom = row[col].strip()
        if symptom != "None" and symptom in all_symptoms:
            idx = all_symptoms.index(symptom)
            weight = severity_df.loc[severity_df["Symptom"] == symptom, "weight"].values[0]
            symptom_vector[idx] = weight
    X.append(symptom_vector)

X_df = pd.DataFrame(X, columns=all_symptoms)
y = df["Disease"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_df, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))

# Save model
with open("model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

print("Model has been saved to model.pkl")
