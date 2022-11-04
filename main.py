#Import libraries
import streamlit as st
import pandas as pd
import numpy as np

DATA_URL = ("\Users\Jacob\OneDrive\Documents\Python\TrafficStreamlit\Motor_Vehicle_Collisions_-_Crashes.csv")

#Title and description
st.title("Vehicle Collisions in New York City")
st.markdown("This application is a Streamlit dashboard that can be used"
    "to analyse motor vehicle collisions in NYC ")

#Cache data to speed up load time
@st.cache(persist=True)

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data

data = load_data(100000)

#Map and slider bar
st.header('Where are the most people injured in NYC?')
injured_people = st.slider('Number of persons injured in vehicle collisions',0, 19)
st.map(data.query('injured_persons >= @injured_people')[['latitude', 'longitude']].dropna(how='any'))





#Show raw data toggle
if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
