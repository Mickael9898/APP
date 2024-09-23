import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load data
url = "https://linked.aub.edu.lb/pkgcube/data/1628de0d6ccf730c607b092724e8128a_20240907_213817.csv"
data = pd.read_csv(url)

# Define columns to use
education_columns = [
    'PercentageofEducationlevelofresidents-university',
    'PercentageofEducationlevelofresidents-vocational',
    'PercentageofEducationlevelofresidents-elementary',
    'PercentageofEducationlevelofresidents-illeterate'
]

# Function to map towns to districts
def map_town_to_district(town_name):
    mount_lebanon = ['Baabda', 'Aabadiyeh', 'Bireh', 'Aarayet', 'Beit Meri', 'Chouf', 'Metn', 'Keserwan',
                     'Jbeil', 'Aley', 'Hadath', 'Hazmieh', 'Fanar', 'Broumana', 'Daher El Souan', 'Bchamoun']
    north_lebanon = ['Aaba', 'AAridet Cheikh Zennad', 'Akkar', 'Tripoli', 'Zgharta', 'Ehden', 'Bcharre',
                     'Koura', 'Batroun', 'Miniyeh', 'Dannieh', 'Qoubayat']
    south_lebanon = ['A\'ain El-Mir (El Establ)', 'Sidon', 'Tyre', 'Jezzine', 'Nabatieh', 'Bint Jbeil', 
                     'Hasbaya', 'Marjayoun', 'Qlaiaa']
    beirut = ['Beirut', 'Ashrafieh', 'Hamra', 'Verdun', 'Gemmayzeh', 'Ain El Mreisseh', 'Furn El Chebbak']
    beqaa = ['Baalbek', 'Zahle', 'Hermel', 'Rachaya', 'Bekaa', 'Qaa', 'Taanayel', 'Chtaura', 'Bar Elias', 
             'Anjar', 'Al Fakeha', 'Qabb Elias']
    
    if any(town in town_name for town in mount_lebanon):
        return 'Mount Lebanon'
    elif any(town in town_name for town in north_lebanon):
        return 'North Lebanon'
    elif any(town in town_name for town in south_lebanon):
        return 'South Lebanon'
    elif any(town in town_name for town in beirut):
        return 'Beirut'
    elif any(town in town_name for town in beqaa):
        return 'Beqaa'
    return 'Mount Lebanon'

dists = data['refArea'].str.split('/').str[4]
data['dists'] = dists
st.write(data)
# Apply mapping function
data['District'] = data['Town'].apply(map_town_to_district)

# Filter out "Other Regions"
data = data[data['District'] != 'Other Regions']

# Clean the data
data_clean = data.dropna(subset=education_columns)
data_clean[education_columns] = data_clean[education_columns].apply(pd.to_numeric, errors='coerce')

# Check if the 'PercentageofEducationlevelofresidents-secondary' column exists
if 'PercentageofEducationlevelofresidents-secondary' not in data_clean.columns:
    st.warning("The 'PercentageofEducationlevelofresidents-secondary' column is missing from the dataset, and will be skipped.")

# Streamlit app layout
st.title("Lebanon Education Levels by District")

# Visualization 1: Box Plot for University Education Levels
st.subheader("Distribution of Education Levels by District")
# fig1 = px.box(data_clean, x='District', y='PercentageofEducationlevelofresidents-university', 
#               title='University Education Levels by District', 
#               labels={'PercentageofEducationlevelofresidents-university': 'University Education Level (%)'})
# st.plotly_chart(fig1)
button1 = st.button('click here')
button2 = st.button('click here for second viz')
if button1:
    fig1 = px.box(data, x='dists', y='PercentageofEducationlevelofresidents-university', 
                  title='University Education Levels by District', 
                  labels={'PercentageofEducationlevelofresidents-university': 'University Education Level (%)'})
    st.plotly_chart(fig1)
elif button2:
    fig1 = px.box(data, x='dists', y='PercentageofEducationlevelofresidents-vocational', 
                  title='Vocational Education Levels by District', 
                  labels={'PercentageofEducationlevelofresidents-vocational': 'Vocational Education Level (%)'})
    st.plotly_chart(fig1)
    

# Visualization 2: Pie Chart of Illetracy Distribution
st.subheader("Education Level by District")
district_edu = data_clean.groupby('District')['PercentageofEducationlevelofresidents-illeterate'].mean().reset_index()
data['PercentageofEducationlevelofresidents-illeterate'] = pd.to_numeric(
    data['PercentageofEducationlevelofresidents-illeterate'], errors='coerce')

# Creating a pie chart for illiteracy percentage across districts
st.title("Illiteracy Percentage Across Districts")

# Group the data by 'dists' (Districts) and get the mean illiteracy percentage per district
data['PercentageofEducationlevelofresidents-illeterate'] = pd.to_numeric(
    data['PercentageofEducationlevelofresidents-illeterate'], errors='coerce')

# Group the data by districts and sum the secondary education percentages
district_secondary_education = data.groupby('dists')['PercentageofEducationlevelofresidents-illeterate'].mean().reset_index()

# Create the pie chart using Plotly Express
fig750 = px.pie(district_secondary_education, 
             values='PercentageofEducationlevelofresidents-illeterate', 
             names='dists',
             title='Illeteracy Percentage by District',
             hole=0.3)  # Optional: Adds a donut-style hole

st.plotly_chart(fig750)

# Visualization 3: Bar chart for education levels in 4 towns in Mount Lebanon
st.subheader("Education Levels in Selected Towns of Mount Lebanon")

# Define the four towns from Mount Lebanon to include
selected_towns = ['Baabda', 'Bireh', 'Beit Meri', 'Chouf']

# Filter data for those towns
mount_lebanon_towns = data_clean[data_clean['Town'].isin(selected_towns)]

# Create a bar chart using Plotly Express for education levels in the selected towns
fig_bar = px.bar(mount_lebanon_towns, 
                 x='Town', 
                 y=education_columns, 
                 title="Education Levels in Selected Mount Lebanon Towns",
                 labels={
                     'value': 'Percentage (%)', 
                     'variable': 'Education Level'
                 },
                 barmode='group')

st.plotly_chart(fig_bar)

# Visualization 4: Bar chart for education levels in Sour and Saaideh with a switch button
st.subheader("Education Levels in Sour and Saaideh")

# Add a selectbox to switch between the two towns
selected_town = st.radio("Select a town", ['Sour', 'Saaideh'])

# Filter data for the selected town
town_data = data_clean[data_clean['Town'] == selected_town]

# Create a bar chart using Plotly Express for education levels in the selected town
fig_town = px.bar(town_data, 
                  x='Town', 
                  y=education_columns, 
                  title=f"Education Levels in {selected_town}",
                  labels={
                      'value': 'Percentage (%)', 
                      'variable': 'Education Level'
                  },
                  barmode='group')

st.plotly_chart(fig_town)
