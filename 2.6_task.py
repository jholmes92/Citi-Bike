import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime as dt
import base64
import io


## Load data ##
df = pd.read_csv('newyork_data_sample.csv', index_col=0)

# Groupby
df['value'] = 1 
df_groupby_bar = df.groupby('start_station_name', as_index=False).agg({'value': 'sum'})
top20 = df_groupby_bar.nlargest(20, 'value')

## Set page title and favicon ##
st.set_page_config(
    page_title="Streamlit Dashboard",
    page_icon=":bike:"
)

## Add a title and descriptive text ##
st.title("Welcome to My Streamlit Dashboard")
st.write("""
This dashboard showcases some visualizations using Streamlit and Plotly.
""")

### Bar chart ###
st.subheader("Top 20 most popular bike stations in New York City")
fig = go.Figure(go.Bar(x=top20['start_station_name'], y=top20['value'], marker={'color': top20['value'], 'colorscale': 'Reds'}))
fig.update_layout(
    xaxis_title='Start stations',
    yaxis_title='Sum of trips',
    width=900, 
    height=600,
    xaxis_tickangle=-25
)
st.plotly_chart(fig)

### Dual axis line chart ###
st.subheader("Daily bike rides and temperature")
fig_line = make_subplots(specs=[[{"secondary_y": True}]])

fig_line.add_trace(
    go.Scatter(x=df['date'], y=df['bike_rides_daily'], name='Daily bike rides'),
    secondary_y=False
)

fig_line.add_trace(
    go.Scatter(x=df['date'], y=df['avgTemp'], name='Daily temperature'),
    secondary_y=True
)

fig_line.update_layout(
    xaxis_title='Date',
    yaxis_title='Count',
    width=900,
    height=600,
    title="Daily Bike Rides and Temperature"
)

st.plotly_chart(fig_line)

### Adding the Map screenshots ###


# Path to your PNG file
file_path = r'C:\Users\repla\OneDrive\Documents\School\Data Visualizations with Python\Citi-Bike\kepler.gl.tripsfilter.png'

# Read the image file as binary data
with open(file_path, 'rb') as f:
    image_bytes = f.read()

# Display the image
st.image(image_bytes, caption='Trips - Filter', use_column_width=True)

# Path to your PNG file
file_path = r'C:\Users\repla\OneDrive\Documents\School\Data Visualizations with Python\Citi-Bike\kepler.gl.startpoint.png'

# Read the image file as binary data
with open(file_path, 'rb') as f:
    image_bytes = f.read()

# Display the image
st.image(image_bytes, caption='Start - Point', use_column_width=True)

# Path to your PNG file
file_path = r'C:\Users\repla\OneDrive\Documents\School\Data Visualizations with Python\Citi-Bike\kepler.gl.endpoint.png'

# Read the image file as binary data
with open(file_path, 'rb') as f:
    image_bytes = f.read()

# Display the image
st.image(image_bytes, caption='End - Point', use_column_width=True)

# Path to your PNG file
file_path = r'C:\Users\repla\OneDrive\Documents\School\Data Visualizations with Python\Citi-Bike\kepler.gl.startend.arc.png'

# Read the image file as binary data
with open(file_path, 'rb') as f:
    image_bytes = f.read()

# Display the image
st.image(image_bytes, caption='Start - End | Arc', use_column_width=True)

# Path to your PNG file
file_path = r'C:\Users\repla\OneDrive\Documents\School\Data Visualizations with Python\Citi-Bike\kepler.gl.startend.line.png'

# Read the image file as binary data
with open(file_path, 'rb') as f:
    image_bytes = f.read()

# Display the image
st.image(image_bytes, caption='Start - End | Line', use_column_width=True)

