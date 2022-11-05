#Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

#Assign data path to variable
DATA_URL = ("\Users\Jacob\OneDrive\Documents\Python\TrafficStreamlit\Traffic-Dashboard\Motor_Vehicle_Collisions_-_Crashes.csv")


#Page title and description
st.title("Vehicle Collisions in New York City")
st.markdown("This application is a Streamlit dashboard to analyse motor vehicle collisions in NYC ")


#Cache data to speed up load time
@st.cache(persist=True)


#Read and clean csv data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data


#Set two data variables, one for later use
data = load_data(100000)
original_data = data


#Map and slider bar
st.header('Where are the most people injured in NYC?')
injured_people = st.slider('Number of persons injured in vehicle collisions',0, 19)
st.map(data.query('injured_persons >= @injured_people')[['latitude', 'longitude']].dropna(how='any'))

#Hour analysis dropdown
st.header('How many collisions occur during a given time of day?')
hour = st.selectbox('Hour to look at', range(0, 24), 1)
data = data[data['date/time'].dt.hour == hour]
st.markdown('Vehicle collisions between %i:00 and %i:00' % (hour, (hour + 1) % 24))


#Use numpy to find geographic midpoint of data to centre map
midpoint = (np.average(data['latitude']), np.average(data['longitude']))


#Create map visuals using pydeck
st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state={
        'latitude': midpoint[0],
        'longitude': midpoint[1],
        'zoom': 11,
        'pitch': 50,
    },
    layers=[
        pdk.layer(
            'HexagonLayer',
            data=data[['date/time', 'latitude', 'longitude']],
            get_position=['latitude', 'longitude'],
            radius=100,
            extruded=True,
            pickable=True,
            elevation_scale=4,
            elevation_range=[0, 1000],
        ),
    ],
))


#Interactive plotly histogram 
st.subheader('Breakdown by minute %i:00 and %i:00' % (hour, (hour + 1) %24))
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour +1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes':hist})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)


#5 most dangerous streets by transport type
st.header('5 most dangerous streets')
select = st.selectbox('Transport used', ['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'Pedestrians':
    st.write(original_data.query('injured_pedestrians >= 1')[['on_street_name', 'injured_pedestrians']].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how='any')[:5])
elif select == 'Cyclists':
    st.write(original_data.query('injured_cyclists >= 1')[['on_street_name', 'injured_cyclists']].sort_values(by=['injured_cyclists'], ascending=False).dropna(how='any')[:5])
else:
    st.write(original_data.query('injured_motorists >= 1')[['on_street_name', 'injured_motorists']].sort_values(by=['injured_motorists'], ascending=False).dropna(how='any')[:5])


#Show raw data toggle
if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
