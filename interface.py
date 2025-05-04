import streamlit as st

def render_form(all_symptoms):
    """
    Renders the form for symptom selection and user details.
    """
    st.subheader("Enter Your Details")
    
    # Input for patient name
    name = st.text_input("Name", placeholder="Enter your name")
    
    # Input for email with validation
    email = st.text_input("Email", placeholder="Enter your email")
    
    # Symptom selection
    st.subheader("Select up to 5 symptoms:")
    symptoms_selected = []
    
    # Allow user to select symptoms
    for i in range(1, 6):
        symptom = st.selectbox(f"Symptom {i}", [""] + all_symptoms, key=f"symptom_{i}")
        if symptom:
            symptoms_selected.append(symptom)

    # Submit button
    submit = st.form_submit_button("Get Diagnosis")
    
    # Display warning if no symptoms are selected
    if submit and not symptoms_selected:
        st.warning("⚠️ Please select at least one symptom.")
    
    return name, email, symptoms_selected, submit
