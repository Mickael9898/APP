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
st.subheader("Distribution of University Education Levels by District")
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
                  title='University Education Levels by District', 
                  labels={'PercentageofEducationlevelofresidents-university': 'University Education Level (%)'})
    st.plotly_chart(fig1)
    

# Visualization 2: Pie Chart of University Education Distribution
st.subheader("University Education Distribution by District")
district_edu = data_clean.groupby('District')['PercentageofEducationlevelofresidents-illeterate'].mean().reset_index()
data['PercentageofEducationlevelofresidents-illeterate'] = pd.to_numeric(
    data['PercentageofEducationlevelofresidents-illeterate'], errors='coerce')

# Creating a pie chart for illiteracy percentage across districts
st.title("Illiteracy Percentage Across Districts")

# Group the data by 'dists' (Districts) and get the mean illiteracy percentage per district
data['PercentageofEducationlevelofresidents-vocational'] = pd.to_numeric(
    data['PercentageofEducationlevelofresidents-vocational'], errors='coerce')

# Group the data by districts and sum the secondary education percentages
district_secondary_education = data.groupby('dists')['PercentageofEducationlevelofresidents-vocational'].mean().reset_index()

# Create the pie chart using Plotly Express
fig750 = px.pie(district_secondary_education, 
             values='PercentageofEducationlevelofresidents-vocational', 
             names='dists',
             title='Secondary Education Percentage by District',
             hole=0.3)  # Optional: Adds a donut-style hole

st.plotly_chart(fig750)

# Visualization 3: Stacked Bar Chart of Education Levels by District
st.subheader("Stacked Bar Chart of Education Levels by District")
district_education_levels = data_clean.groupby('District')[education_columns].mean().reset_index()

fig3 = go.Figure()
fig3.add_trace(go.Bar(x=district_education_levels['District'], y=district_education_levels['PercentageofEducationlevelofresidents-university'], name='University Education', marker_color='indianred'))

# Only add secondary education if the column exists
if 'PercentageofEducationlevelofresidents-secondary' in data_clean.columns:
    fig3.add_trace(go.Bar(x=district_education_levels['District'], y=district_education_levels['PercentageofEducationlevelofresidents-secondary'], name='Secondary Education', marker_color='lightsalmon'))

fig3.add_trace(go.Bar(x=district_education_levels['District'], y=district_education_levels['PercentageofEducationlevelofresidents-vocational'], name='Vocational Education', marker_color='lightseagreen'))
fig3.add_trace(go.Bar(x=district_education_levels['District'], y=district_education_levels['PercentageofEducationlevelofresidents-elementary'], name='Elementary Education', marker_color='lightblue'))

fig3.update_layout(barmode='stack', title='Education Levels by District', xaxis_title='District', yaxis_title='Percentage (%)', legend_title='Education Level')
st.plotly_chart(fig3)

# Visualization 4: Line Chart of Education Levels
st.subheader("Education Levels Across Districts")
district_avg_education = data_clean.groupby('District')[education_columns].mean().reset_index()

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=district_avg_education['District'], y=district_avg_education['PercentageofEducationlevelofresidents-university'], mode='lines+markers', name='University Education', line=dict(color='blue')))
fig4.add_trace(go.Scatter(x=district_avg_education['District'], y=district_avg_education['PercentageofEducationlevelofresidents-vocational'], mode='lines+markers', name='Vocational Education', line=dict(color='green')))
fig4.add_trace(go.Scatter(x=district_avg_education['District'], y=district_avg_education['PercentageofEducationlevelofresidents-elementary'], mode='lines+markers', name='Elementary Education', line=dict(color='orange')))
fig4.add_trace(go.Scatter(x=district_avg_education['District'], y=district_avg_education['PercentageofEducationlevelofresidents-illeterate'], mode='lines+markers', name='Illiteracy', line=dict(color='red')))

fig4.update_layout(title='Education Levels Across Districts', xaxis_title='District', yaxis_title='Percentage (%)', legend_title='Education Level')
st.plotly_chart(fig4)
