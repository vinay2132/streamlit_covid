import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

st.write("## COVID-19 Healthy Diet Dataset")

# Dropdown (selectbox) options
options = [
    'Fat_Supply_Quantity_Data.csv', 
    'Food_Supply_kcal_Data.csv', 
    'Food_Supply_Quantity_kg_Data.csv', 
    'Protein_Supply_Quantity_Data.csv', 
    'Supply_Food_Data_Descriptions.csv'
]

# Create a dropdown in Streamlit
selected_option = st.selectbox('Choose an option:', options)

# Display the selected option
st.write(f"Your selected file is `{selected_option}`")

# Load the selected CSV file
data_path = f"archive/{selected_option}"
try:
    data = pd.read_csv(data_path)
    st.write(data)
except FileNotFoundError:
    st.error(f"File `{data_path}` not found. Please make sure the file exists in the specified directory.")

# Dropdown for state options
state_options = ['Confirmed', 'Deaths', 'Active', 'Mortality']
selected_state_option = st.selectbox('Choose a state option:', state_options)

# Load the main dataset
try:
    food = pd.read_csv("archive/Food_Supply_kcal_Data.csv")
    food['Mortality'] = food['Deaths'] / food['Confirmed']
except FileNotFoundError:
    st.error("Main dataset file `Food_Supply_kcal_Data.csv` not found.")
else:
    # Create a Plotly bar chart
    fig = px.bar(food, x="Country", y=selected_state_option).update_xaxes(categoryorder="total descending")
    st.plotly_chart(fig)

    # Remove rows where 'Active' has NaN values
    food = food[food['Active'].notna()]

    # Create a scatter plot excluding Yemen
    fig = px.scatter(
        food[food.Country != 'Yemen'], 
        x="Mortality", 
        y="Obesity", 
        size="Active", 
        hover_name='Country', 
        log_x=False, 
        size_max=30, 
        template="simple_white"
    )

    # Add a horizontal line representing the mean of 'Obesity'
    fig.add_shape(
        type="line",
        x0=0,
        y0=food[food.Country != 'Yemen']['Obesity'].mean(),
        x1=food[food.Country != 'Yemen']['Mortality'].max(),
        y1=food[food.Country != 'Yemen']['Obesity'].mean(),
        line=dict(
            color="crimson",
            width=4
        )
    )

    st.plotly_chart(fig)

    # Calculate the mean intake of food sources across all countries
    diet_mean = food.describe().iloc[1]
    diet_mean = pd.DataFrame(diet_mean, columns=['mean'])

    # Drop columns that are not relevant to food intake analysis
    diet_mean = diet_mean.drop(['Deaths', 'Population', 'Undernourished', 'Obesity', 'Recovered', 'Confirmed', 'Active'], axis=0, errors='ignore')

    # Sort the food sources by mean intake in descending order and select the top 10
    diet_mean = diet_mean.sort_values(by='mean', ascending=False).iloc[:10]

    # Plot the top 10 food sources as a pie chart
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    diet_mean.plot.pie(
        y='mean',
        ax=ax,
        autopct='%1.1f%%',
        legend=False,
        startangle=90,
        title="Mean Intake of Top 10 Food Sources",
        colors=plt.cm.tab10.colors
    )

    ax.set_title("Mean Intake of Top 10 Food Sources", color='white', fontsize=16)
    plt.setp(ax.texts, color='white')

    st.pyplot(fig)

    
