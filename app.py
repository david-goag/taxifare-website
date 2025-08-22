import streamlit as st
import datetime
import requests
import pandas as pd

import folium
import streamlit as st

from streamlit_folium import st_folium

'''
# TaxiFareModel front
'''

st.markdown('''

Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare-505391779697.europe-southwest1.run.app/'

if url == 'https://taxifare-505391779697.europe-southwest1.run.app/':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
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
st.write('Pickup Longitude: ', pickup_longitude_input)

passenger_count = st.slider('Select a pickup_datetime', 1, 8, 2)
st.write("Number of passengers: ", passenger_count)




url = 'https://taxifare-505391779697.europe-southwest1.run.app/predict?'

pickup_longitude = -73.950655
pickup_latitude = 40.783282
dropoff_longitude = -73.984365
dropoff_latitude = 40.769802

#pickup_df = pd.DataFrame({'lon': [pickup_longitude], 'lat': [pickup_latitude]})
#dropoff_df = pd.DataFrame({'lon': [dropoff_longitude], 'lat': [dropoff_latitude]})
map_df = pd.DataFrame({'lon': [pickup_longitude, dropoff_longitude], 'lat': [pickup_latitude, dropoff_latitude], "color": ["#00ff00", "#ffff00"], "location": ["Pickup", "Dropoff"]})

#st.map(pickup_df)
#st.map(dropoff_df, color="#ffff00")
#st.map(map_df, color=map_df["color"])



"""# center on Liberty Bell, add marker
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282]#[39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)"""

m = folium.Map(location=[(pickup_latitude+dropoff_latitude)/2, (pickup_longitude+dropoff_longitude)/2], zoom_start=12)
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
st_data = st_folium(m, width=725)

params = {
        "pickup_datetime":pickup_datetime,
        "pickup_longitude":pickup_longitude,
        "pickup_latitude":pickup_latitude,
        "dropoff_longitude":dropoff_longitude,
        "dropoff_latitude":dropoff_latitude,
        "passenger_count":passenger_count
    }

response = requests.get(url, params=params)

st.write("Fare: ", response.json()["fare"])
