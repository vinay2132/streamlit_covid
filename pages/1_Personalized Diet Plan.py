import streamlit as st
import pandas as pd

# Streamlit App Title
st.write("# Personalized Diet Plan")

# Load dataset
@st.cache_data  # Cache the data for performance optimization
def load_data():
    return pd.read_csv("archive/Food_Supply_kcal_Data.csv")

data = load_data()

# App Introduction
st.subheader("Create a dynamic diet plan based on your health, preferences, and COVID-19 recovery status")

# Input Form
with st.form("diet_form"):
    st.header("Customer Information")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    age_group = st.selectbox("Age Group", ["Child", "Adult", "Elderly"])
    gender = st.radio("Gender", ("Male", "Female", "Other"))
    weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
    height = st.number_input("Height (cm)", min_value=1.0, step=0.1)
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Moderately Active", "Highly Active"])
    
    st.header("Health Metrics")
    obesity_status = st.radio("Obesity Status", ["Underweight", "Normal", "Overweight", "Obese"])
    health_conditions = st.multiselect(
        "Existing Health Conditions",
        ["Diabetes", "Hypertension", "Cardiovascular Diseases", "Other", "None"]
    )
    
    st.header("COVID-19 Related Information")
    infection_status = st.radio("Confirmed COVID-19 Case?", ["Yes", "No"])
    active_symptoms = st.multiselect(
        "Active Symptoms (if applicable)", 
        ["Fever", "Cough", "Fatigue", "None"], 
        disabled=(infection_status == "No")
    )
    recovery_status = st.radio("Recovery Status", ["Recovering", "Post-Recovery", "Not Applicable"], disabled=(infection_status == "No"))
    symptom_severity = st.radio(
        "Severity of Symptoms", 
        ["Mild", "Moderate", "Severe"], 
        disabled=(infection_status == "No")
    )
    vaccination_status = st.radio("Vaccination Status", ["Yes", "No"])
    
    st.header("Dietary Preferences")
    dietary_restrictions = st.multiselect(
        "Dietary Restrictions", 
        ["Vegetarian", "Vegan", "Non-Vegetarian", "Gluten-Free", "Lactose-Free", "None"]
    )
    allergies = st.multiselect("Allergies", ["Nuts", "Dairy", "Gluten", "Other", "None"])
    cultural_practices = st.text_input("Cultural or Religious Dietary Practices (if any)")
    preferred_food_categories = st.multiselect(
        "Preferred Food Categories", 
        ["Fruits", "Vegetables", "Cereals", "Dairy", "Meat", "Seafood", "Other"]
    )
    
    st.header("Lifestyle Factors")
    daily_calorie_goal = st.number_input("Daily Calorie Intake Goal (if known)", min_value=500, step=100)
    
    st.header("Mental Health and Stress")
    stress_level = st.slider("Stress Level (1 = Low, 10 = High)", 1, 10)
    mood_needs = st.text_input("Mood-related dietary needs (e.g., foods to reduce stress)")
    
    st.header("Additional Factors")
    food_access = st.text_area("Access to Specific Food Categories (e.g., fresh fruits, cereals, etc.)")
    budget = st.number_input("Budget for Meal Planning (in USD)", min_value=0, step=1)
    country = st.selectbox("Country", data['Country'].unique())

    # Form Submit Button
    submit_button = st.form_submit_button(label="Generate Diet Plan")

# Process and Display the Diet Plan
if submit_button:
    st.success(f"Generating diet plan for {name}...")
    
    # Calculate BMI
    bmi = round(weight / ((height / 100) ** 2), 2)
    bmi_status = (
        "Underweight" if bmi < 18.5 else 
        "Normal" if bmi < 25 else 
        "Overweight" if bmi < 30 else 
        "Obese"
    )
    # st.write(f"**Your BMI:** {bmi} ({bmi_status})")
    
    # Filter data based on selected country
    country_data = data[data['Country'] == country]
    if not country_data.empty:
        st.subheader("Your Personalized Diet Plan")
        st.write("Based on your preferences, health metrics, and selected country:")
        for food_group in [
            "Fruits - Excluding Wine", "Vegetables", "Cereals - Excluding Beer", 
            "Milk - Excluding Butter", "Meat", "Eggs", "Fish, Seafood"
        ]:
            recommended_amount = country_data[food_group].values[0]
            st.write(f"- **{food_group}:** {recommended_amount} kcal (Recommended)")
        
        st.write(f"**Daily Calorie Goal:** {daily_calorie_goal} kcal")
        if stress_level >= 7:
            st.warning("High stress level detected. Consider foods that help reduce stress, like dark chocolate, nuts, or tea.")
    else:
        st.warning("No data available for your selected country!")
