# import streamlit as st
# import pandas as pd

# # Streamlit App Title
# st.write("# Personalized Diet Plan")

# # Load dataset
# @st.cache_data  # Cache the data for performance optimization
# def load_data():
#     return pd.read_csv("archive/Food_Supply_kcal_Data.csv")

# data = load_data()

# # App Introduction
# st.subheader("Create a dynamic diet plan based on your health, preferences, and COVID-19 recovery status")

# # Input Form
# with st.form("diet_form"):
#     st.header("Customer Information")
#     name = st.text_input("Name")
#     age = st.number_input("Age", min_value=1, max_value=120, step=1)
#     age_group = st.selectbox("Age Group", ["Child", "Adult", "Elderly"])
#     gender = st.radio("Gender", ("Male", "Female", "Other"))
#     weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
#     height = st.number_input("Height (cm)", min_value=1.0, step=0.1)
#     activity_level = st.selectbox("Activity Level", ["Sedentary", "Moderately Active", "Highly Active"])
    
#     st.header("Health Metrics")
#     obesity_status = st.radio("Obesity Status", ["Underweight", "Normal", "Overweight", "Obese"])
#     health_conditions = st.multiselect(
#         "Existing Health Conditions",
#         ["Diabetes", "Hypertension", "Cardiovascular Diseases", "Other", "None"]
#     )
    
#     st.header("COVID-19 Related Information")
#     infection_status = st.radio("Confirmed COVID-19 Case?", ["Yes", "No"])
#     active_symptoms = st.multiselect(
#         "Active Symptoms (if applicable)", 
#         ["Fever", "Cough", "Fatigue", "None"], 
#         disabled=(infection_status == "No")
#     )
#     recovery_status = st.radio("Recovery Status", ["Recovering", "Post-Recovery", "Not Applicable"], disabled=(infection_status == "No"))
#     symptom_severity = st.radio(
#         "Severity of Symptoms", 
#         ["Mild", "Moderate", "Severe"], 
#         disabled=(infection_status == "No")
#     )
#     vaccination_status = st.radio("Vaccination Status", ["Yes", "No"])
    
#     st.header("Dietary Preferences")
#     dietary_restrictions = st.multiselect(
#         "Dietary Restrictions", 
#         ["Vegetarian", "Vegan", "Non-Vegetarian", "Gluten-Free", "Lactose-Free", "None"]
#     )
#     allergies = st.multiselect("Allergies", ["Nuts", "Dairy", "Gluten", "Other", "None"])
#     cultural_practices = st.text_input("Cultural or Religious Dietary Practices (if any)")
#     preferred_food_categories = st.multiselect(
#         "Preferred Food Categories", 
#         ["Fruits", "Vegetables", "Cereals", "Dairy", "Meat", "Seafood", "Other"]
#     )
    
#     st.header("Lifestyle Factors")
#     daily_calorie_goal = st.number_input("Daily Calorie Intake Goal (if known)", min_value=500, step=100)
    
#     st.header("Mental Health and Stress")
#     stress_level = st.slider("Stress Level (1 = Low, 10 = High)", 1, 10)
#     mood_needs = st.text_input("Mood-related dietary needs (e.g., foods to reduce stress)")
    
#     st.header("Additional Factors")
#     food_access = st.text_area("Access to Specific Food Categories (e.g., fresh fruits, cereals, etc.)")
#     budget = st.number_input("Budget for Meal Planning (in USD)", min_value=0, step=1)
#     country = st.selectbox("Country", data['Country'].unique())

#     # Form Submit Button
#     submit_button = st.form_submit_button(label="Generate Diet Plan")

# # Process and Display the Diet Plan
# if submit_button:
#     st.success(f"Generating diet plan for {name}...")
    
#     # Calculate BMI
#     bmi = round(weight / ((height / 100) ** 2), 2)
#     bmi_status = (
#         "Underweight" if bmi < 18.5 else 
#         "Normal" if bmi < 25 else 
#         "Overweight" if bmi < 30 else 
#         "Obese"
#     )
#     # st.write(f"**Your BMI:** {bmi} ({bmi_status})")
    
#     # Filter data based on selected country
#     country_data = data[data['Country'] == country]
#     if not country_data.empty:
#         st.subheader("Your Personalized Diet Plan")
#         st.write("Based on your preferences, health metrics, and selected country:")
#         for food_group in [
#             "Fruits - Excluding Wine", "Vegetables", "Cereals - Excluding Beer", 
#             "Milk - Excluding Butter", "Meat", "Eggs", "Fish, Seafood"
#         ]:
#             recommended_amount = country_data[food_group].values[0]
#             st.write(f"- **{food_group}:** {recommended_amount} kcal (Recommended)")
        
#         st.write(f"**Daily Calorie Goal:** {daily_calorie_goal} kcal")
#         if stress_level >= 7:
#             st.warning("High stress level detected. Consider foods that help reduce stress, like dark chocolate, nuts, or tea.")
#     else:
#         st.warning("No data available for your selected country!")

import streamlit as st
import pandas as pd
import openai
from transformers import pipeline  
# Hugging Face pipeline for weekly plan

openai.api_key = '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'
@st.cache_data
def load_dataset(file_path):
    """Loads a dataset from a CSV file and caches it for faster access."""
    return pd.read_csv(file_path)

# Loading datasets and caching them
fat_data = load_dataset('archive/Fat_Supply_Quantity_Data.csv')
protein_data = load_dataset('archive/Protein_Supply_Quantity_Data.csv')
food_kcal_data = load_dataset('archive/Food_Supply_kcal_Data.csv')
quantity_data = load_dataset('archive/Food_Supply_Quantity_kg_Data.csv')
food_descriptions = load_dataset('archive/Supply_Food_Data_Descriptions.csv')

@st.cache_data
def recommend_foods(covid_conditions, diet_preferences, calorie_target):
    """Generates recommendations based on filtered datasets."""
    recommendations = []
    for preference in diet_preferences:
        matching_foods = food_descriptions[food_descriptions['Categories'].str.contains(preference, case=False, na=False)]
        recommendations.append(matching_foods)

    food_kcal_data['Unit (all except Population)'] = pd.to_numeric(food_kcal_data['Unit (all except Population)'], errors='coerce')
    calorie_based = food_kcal_data[food_kcal_data['Unit (all except Population)'] <= calorie_target]
    recommendations.append(calorie_based)
    
    final_recommendations = pd.concat(recommendations).drop_duplicates()
    return final_recommendations

def gpt_diet_plan(covid_conditions, diet_preferences, calorie_target, dataset):
    """Generates a diet plan using GPT based on user inputs and dataset."""
    try:
        food_list = "\n".join([f"{i+1}. {row['Items']} - Category: {row['Categories']}" for i, row in dataset.iterrows()])
        
        prompt = f"""
        Based on the following foods, generate a balanced diet plan for a person with these conditions: {', '.join(covid_conditions)}.
        Preferences: {', '.join(diet_preferences)}.
        Calorie target: {calorie_target} kcal.

        Foods available:
        {food_list}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a dietitian assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error generating diet plan: {str(e)}"

def generate_weekly_plan(daily_plan):
    """Generate a weekly plan from a daily plan using Hugging Face."""
    weekly_plan = "\n".join([f"Day {i+1}: {daily_plan}" for i in range(7)])
    return weekly_plan

# Streamlit UI
st.header("Personalized Diet Plan Generator")

# Collecting full name and weight
full_name = st.text_input("Enter your full name:")
weight = st.number_input("Enter your weight (in kgs):", min_value=30, max_value=200, step=1)

covid_conditions = st.multiselect(
    "Select your COVID-related conditions:",
    ["Fatigue", "Fever", "Loss of Appetite", "Cough", "Body Pain", "Other"]
)

diet_preferences = st.multiselect(
    "Select your dietary preferences:",
    ["Vegetarian", "Vegan", "High Protein", "Low Fat", "Gluten-Free", "Dairy-Free"]
)

calorie_target = st.slider(
    "Daily Calorie Target (in kcal):",
    min_value=1000, max_value=3000, value=2000, step=100
)

if st.button("Generate Diet Plan"):
    diet_plan = recommend_foods(covid_conditions, diet_preferences, calorie_target)
    
    # GPT-based recommendations
    st.subheader("AI-Generated Diet Plan")
    diet_plan_gpt = gpt_diet_plan(covid_conditions, diet_preferences, calorie_target, food_descriptions)
    st.write(diet_plan_gpt)
    
    # Weekly plan generation
    weekly_plan = generate_weekly_plan(diet_plan_gpt)
    st.subheader("Weekly Plan")
    st.text(weekly_plan)
    
    # Download Options
    csv = diet_plan.to_csv(index=False)
    st.download_button(
        label="Download Dataset-Based Plan as CSV",
        data=csv,
        file_name="dataset_based_diet_plan.csv",
        mime="text/csv",
    )
    
    st.download_button(
        label="Download AI-Generated Plan as Text",
        data=diet_plan_gpt,
        file_name="ai_generated_diet_plan.txt",
        mime="text/plain",
    )
    
    st.download_button(
        label="Download Weekly Plan as Text",
        data=weekly_plan,
        file_name="weekly_diet_plan.txt",
        mime="text/plain",
    )
