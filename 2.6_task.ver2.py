import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime as dt
import base64
import io

# Load data
df = pd.read_csv('newyork_data_sample.csv', index_col=0)

# Groupby start stations
df['value'] = 1 
df_groupby_bar = df.groupby('start_station_name', as_index=False).agg({'value': 'sum'})
top20 = df_groupby_bar.nlargest(20, 'value')

# Set page configuration
st.set_page_config(
    page_title="Streamlit Dashboard",
    page_icon=":bike:"
)

# Add a title and descriptive text
st.title("Analyzing Citi Bike Data for Improved Distribution Strategy in NYC")
st.write("""
Welcome to the Citi Bike Distribution Analysis Dashboard. As the lead analyst for a bike-sharing service based in New York City, our objective is to conduct a descriptive analysis of existing data from Citi Bike facilities. Our goal is to uncover actionable insights to address distribution issues, ensuring a seamless experience for our users and further solidifying our position as a leader in eco-friendly transportation solutions in the city.

Context: Citi Bike has experienced increased popularity, particularly since the Covid–19 pandemic, leading to higher demand and distribution challenges. This dashboard serves as a tool to diagnose distribution issues and provide informed recommendations to enhance our logistics model.

Let's explore the data and discover insights to optimize our bike distribution strategy.
""")


# Bar chart
st.subheader("Top 20 most popular bike stations in New York City")
st.write("""
This bar chart shows the top 20 most popular bike stations in New York City based on the number of trips. Understanding the popularity of these stations is crucial for assessing distribution patterns and identifying areas for improvement in our logistics model.
""")
with st.container():
    fig = go.Figure(go.Bar(
        x=top20['start_station_name'],
        y=top20['value'],
        marker={'color': top20['value'], 'colorscale': 'Reds'}
    ))
    fig.update_layout(
        xaxis_title='Start stations',
        yaxis_title='Sum of trips',
        width=900, 
        height=600,
        xaxis_tickangle=-25
    )
    st.plotly_chart(fig)
    
    # Insights
    st.subheader("Insights")
    st.write("""
    - The colors of the chart are at their darkest as we get to the highest reporting trip stations. For example, West 21st Street and 6th Avenue lead with well over 3000 trips. Therefore, this route is a deep, dark red. On the far right, you can see 9th Avenue and West 22nd Street is a faint white with a hint of red. This indicates it is one of the lowest on the graph, reporting just over 2000 trips.
    - Over 75% of the options displayed in this graph reported somewhere between 2000 and 2500 trips. Our top 25% report exceptional numbers, but do not represent the type of trip numbers we see most of these locations producing.
    """)


# Dual axis line chart
st.subheader("Daily Bike Rides and Temperature Trends")
st.write("""
This interactive chart illustrates the daily trends of bike rides and temperature in New York City. Understanding the relationship between these two factors is essential for analyzing user behavior and identifying potential correlations with distribution challenges.

Bike rides: Represents the daily count of bike rides, reflecting user demand and usage patterns.
Temperature: Indicates the daily average temperature, which may influence user preferences and biking activity.

By examining these trends together, we can gain insights into how weather conditions impact bike usage and distribution patterns, aiding in the formulation of informed strategies for addressing availability issues and optimizing bike distribution across the city.
""")
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

# Insights
st.subheader("Insights")
st.write("""
- To be completely transparent with everyone, I find this chart extremely confusing to interpret with just a quick glance. A bar chart may have been a smarter approach, and we will consider that next time.
- That said, there is a clear arch we can see the chart take as we move left to right. Looking at the timeline, the count, and temperatures, we can see that our trips grow substantially over the spring & summer months. This analysis is consistent with what we already knew but could be used to understand just how much greater it is than in the fall and winter.
""")



# Adding map screenshots
image_info = {
    'kepler.gl.tripsfilter.png': ('Trips', 'In this image, we can see how the created Trips filter can be used to reduce the amount of routes down to only a handful. This allows us to see what our most popular routes are.'),
    'kepler.gl.startpoint.png': ('Starting Point', 'In this image, we can see points on our map that indicate the starting position of one of our routes.'),
    'kepler.gl.endpoint.png': ('Ending Point', 'In this image, we can see points on our map that indicate the ending position of one of our routes.'),
    'kepler.gl.startend.arc.png': ('Start to End | Arc', 'In this image, we can see both the starting, and ending points of a route with an illustrated arc connecting the two points.'),
    'kepler.gl.startend.line.png': ('Start to End | Line', 'In this image, we can see both the starting, and ending points of a route with an illustrated line connecting the two points. ')
}

for image_path, (title, description) in image_info.items():
    # Read the image file as binary data
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    # Display the image with a title and description
    st.image(image_bytes, caption=title, use_column_width=True)
    st.write(description)

# Insights
st.subheader("Insights")
st.write("""
- There are 3 main takeaways from these images. First, in the 'Trips' image, we can see clearly where our top 10 or so most popular routes are located. This allows us to understand why that might be as additional geographical analysis can be made around those addresses
-  Secondly, the 'Starting Point' image gives us a clear idea of where we not only are covering in NYC but where it becomes brighter and more dense. This means certain areas have more riders, which means the need for more units, more opportunity, and ultimately, more sales.
- Lastly, I'd like to direct your attention to the 'Start to End | Arc' image. We can see that in the center of the city, there is a large swath of rides that leave the downtown core and move outward. We can learn from this, and use similar visualizations on the map to determine our locations that require the greatest need, and as I mentioned in the last point, the most sales.
""")