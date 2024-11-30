import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.write("##  COVID-19 Healthy Diet Dataset")

# Dropdown (selectbox) options
options = ['Fat_Supply_Quantity_Data.csv', 'Food_Supply_kcal_Data.csv', 'Food_Supply_Quantity_kg_Data.csv', 'Protein_Supply_Quantity_Data.csv', 'Supply_Food_Data_Descriptions.csv']

# Create a dropdown in Streamlit
selected_option = st.selectbox('Choose an option:', options)

# Display the selected option
st.write(f"Your select file is `{selected_option}`")


# Load the selected CSV file
data_path = f"archive/{selected_option}"  # Correcting the file path string formatting
try:
    data = pd.read_csv(data_path)  # Reading the CSV file
    st.write(data)  # Displaying the data
except FileNotFoundError:
    st.error(f"File `{data_path}` not found. Please make sure the file exists in the specified directory.")





state_options = ['Confirmed', 'Deaths', 'Active', 'Mortality']

# Create a dropdown in Streamlit
selected_state_option = st.selectbox('Choose an option:', state_options)


food = pd.read_csv("archive/Food_Supply_kcal_Data.csv")  

food['Mortality'] = food['Deaths']/food['Confirmed']

# Create a Plotly bar chart
fig = px.bar(food, x="Country", y=selected_state_option).update_xaxes(categoryorder="total descending")

# Use Streamlit to display the Plotly figure
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

# Use Streamlit to display the Plotly figure
st.plotly_chart(fig)

