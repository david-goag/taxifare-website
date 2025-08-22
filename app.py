import streamlit as st
import datetime
import requests
import pandas as pd

import folium
from streamlit_folium import st_folium
import random

'''
# David-goag's TaxiFareModel
'''


pickup_date = st.date_input("Select the travel day:", datetime.datetime.today())
pickup_time = st.time_input('Select the pickup time', datetime.datetime.now())#, step=datetime.timedelta(0:15:00))
pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)
st.write(f"Pickup at {pickup_datetime}")

pickup_longitude = -73.950655
pickup_latitude = 40.783282
dropoff_longitude = -73.984365
dropoff_latitude = 40.769802

pickup_longitude_input = st.number_input('Select the Pickup Longitude:', format="%0.6f", value=pickup_longitude)
#st.write('Pickup Longitude: ', pickup_longitude_input)

pickup_latitude_input = st.number_input('Select the Pickup Latitude:', format="%0.6f", value=pickup_latitude)
#st.write('Pickup Latitude: ', pickup_latitude_input)

dropoff_longitude_input = st.number_input('Select the Dropoff Longitude:', format="%0.6f", value=dropoff_longitude)
#st.write('Dropoff Longitude: ', dropoff_longitude_input)

dropoff_latitude_input = st.number_input('Select the Dropoff Latitude:', format="%0.6f", value=dropoff_latitude)
#st.write('Dropoff Latitude: ', dropoff_latitude_input)

passenger_count = st.slider('Select the number of passengers', 1, 8, 2)
#st.write("Number of passengers: ", passenger_count)


#pickup_df = pd.DataFrame({'lon': [pickup_longitude], 'lat': [pickup_latitude]})
#dropoff_df = pd.DataFrame({'lon': [dropoff_longitude], 'lat': [dropoff_latitude]})
map_df = pd.DataFrame({'lon': [pickup_longitude_input, dropoff_longitude_input], 'lat': [pickup_latitude_input, dropoff_latitude_input], "color": ["#00ff00", "#ffff00"], "location": ["Pickup", "Dropoff"]})

#st.map(pickup_df)
#st.map(dropoff_df, color="#ffff00")


url = 'https://taxifare-505391779697.europe-southwest1.run.app/predict?'

params = {
        "pickup_datetime":pickup_datetime,
        "pickup_longitude":pickup_longitude_input,
        "pickup_latitude":pickup_latitude_input,
        "dropoff_longitude":dropoff_longitude_input,
        "dropoff_latitude":dropoff_latitude_input,
        "passenger_count":passenger_count
    }

response = requests.get(url, params=params)

#st.write("Fare: ", response.json()["fare"])
names = ["Aarav", "Kabir", "Vivaan", "Mandeep", "Reyansh", "Vihaan"] #random.choice(names)
f'''
# Le debes **{round(response.json()["fare"], 2)}**$ a {names[3]}.
'''

m = folium.Map(location=[(pickup_latitude+dropoff_latitude)/2, (pickup_longitude+dropoff_longitude)/2], zoom_start=14)
for i in range(0,len(map_df)):
   folium.Marker(
      location=[map_df.iloc[i]['lat'], map_df.iloc[i]['lon']],
      popup=map_df.iloc[i]['location'],
      icon=folium.DivIcon(html=f"""
            <div><svg>
                <circle cx="20" cy="20" r="20" fill={map_df.iloc[i]['color']} opacity=".4"/>
            </svg></div>""")
   ).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=700, height=350)
