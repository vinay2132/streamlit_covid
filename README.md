# Diet Plan Assistant for COVID-19 Recovery using Virtual Reality and Fine-Tuning

## Overview
This project explores the relationship between dietary patterns and health metrics during the COVID-19 pandemic, offering a range of interactive tools for data analysis and personalized recommendations. It includes three core applications:

### 1. COVID-19 Healthy Diet Dataset Analysis
- Interactive dashboard for visualizing global food supply, nutrition metrics, and their correlation with COVID-19 health data.

### 2. Personalized Diet Plan Generator
- Generates dynamic diet plans tailored to user health metrics, dietary preferences, and country-specific food availability.

### 3. Virtual Reality AI Assistant
- **Training for Professionals**: Physicians and nurses can enhance their skills in diagnosis, emergency response, and surgery through AI-powered virtual reality simulations.
- **Therapeutic Applications**: Provides mental health therapies such as exposure therapy for phobias or PTSD treatment.
- **Patient Support**: Assists patients with physical therapy exercises, meditation, and pre-surgery education.
- **Additional Features**: Gaming tools, mental health quizzes, and diet plan generation.

---

## Features

### 1. COVID-19 Healthy Diet Dataset
- Visualizes global food supply and nutrition metrics during the pandemic.
- Interactive visualizations using Plotly for enhanced analysis.
- Handles missing data with KNNImputer for consistent statistical insights.

### 2. Personalized Diet Plan Generator
- Personalizes diet plans based on user inputs:
  - **Details**: Age, gender, activity level.
  - **Health Metrics**: Obesity, recovery status.
  - **Country-Specific Data**: Food supply.
- Includes stress-level analysis with dietary suggestions for mood improvement.

### 3. Virtual Reality AI Assistant
- Responds to user queries and provides health, diet analysis, and educational information.
- Includes speech-to-text recognition for seamless interaction.

---

## Prerequisites

### Software Requirements
- **Python**: 3.8+
- **Jupyter Notebook**: For running `.ipynb` files interactively.
- **Streamlit**: For launching web-based interactive apps.

### VR Development Engines
- **Unity3D**: For creating VR apps and games.

### 3D Design and Modeling Tools
- **Blender**: Open-source 3D modeling software for VR assets.
- **Autodesk Maya/3ds Max**: Advanced 3D creations.
- **SketchUp**: Architectural designing for VR.

### Python Libraries
Ensure the following libraries are installed:
- `numpy`
- `pandas`
- `seaborn`
- `matplotlib`
- `plotly`
- `scikit-learn`
- `streamlit`

---

## Dataset
Datasets are stored in the `archive/` directory. Required files:
- `Food_Supply_kcal_Data.csv`
- `Fat_Supply_Quantity_Data.csv`
- `Protein_Supply_Quantity_Data.csv`

---

## Installation Steps
1. Place the `archive/` folder in the root directory of the project.
2. Run the respective applications using the commands below:

### COVID-19 Healthy Diet Dataset
```bash
streamlit run src/dataset.py
```

### Personalized Diet Plan Generator
```bash
streamlit run src/1_Personalized\ Diet\ Plan.py
```

---

## Application Details

### 1. COVID-19 Healthy Diet Dataset (`src/dataset.py`)
#### Features:
- Dropdown menu to select and view datasets.
- Plotly bar charts and scatter plots for insights:
  - Mortality and obesity correlations.
  - Active cases, confirmed cases, and deaths by country.
- Includes a mean obesity trend line for better visualization.

#### Usage:
1. Select a dataset from the dropdown.
2. Explore visualizations based on health metrics (Confirmed, Deaths, Mortality, Active).
3. Analyze correlations between mortality and obesity rates.

### 2. Personalized Diet Plan Generator (`src/1_Personalized Diet Plan.py`)
#### Features:
- User input form for:
  - Personal details (age, weight, height, etc.).
  - Health metrics (dietary restrictions, COVID-19 recovery status).
  - Lifestyle factors (activity level, calorie goal, budget).
- Generates personalized food recommendations using country-specific supply data.
- Suggests stress-relieving foods for high-stress levels.

#### Usage:
1. Fill in the form and click "Generate Diet Plan."
2. View personalized recommendations and insights.

### 3. Virtual AI Assistant
#### Setup:
1. Install Unity 3D and connect to Unity Cloud.
2. Import the project from disk with asset installations and VR libraries.
3. Launch the virtual environment to interact with:
   - AI Assistant chatbot with speech-to-text conversion.
   - Features like gaming, mental health quizzes, and diet plan generation.

---
