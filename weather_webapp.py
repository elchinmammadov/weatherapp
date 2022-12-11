#CODE FOR STREAMLIT WWEB APP


# This code downloads current weather data and forecasts from https://openweathermap.org/forecast5 for St Albans, then shows results on Streamlit web app
# My API key: 4d9e86afd3e0034d2ad0b63e6c30da28
# current weather API is explained here: https://openweathermap.org/current
# forecast weather API is explained here: https://openweathermap.org/forecast5
# creating web app with Streamlit https://www.youtube.com/watch?v=ZDffoP6gjxc&t
# deploying web app to Heroku is explained here https://www.youtube.com/watch?v=nJHrSvYxzjE&t

# current weather by city name:   api.openweathermap.org/data/2.5/weather?q=St Albans&units=metric&limit=1&appid=4d9e86afd3e0034d2ad0b63e6c30da28
# current weather by lat & long:   api.openweathermap.org/data/2.5/weather?lat=51.7564&lon=-0.3519&units=metric&limit=1&appid=4d9e86afd3e0034d2ad0b63e6c30da28
# forecast weather by city name:   api.openweathermap.org/data/2.5/forecast?q=St Albans&units=metric&limit=1&appid=4d9e86afd3e0034d2ad0b63e6c30da28
# forecast weather by lat & long:   api.openweathermap.org/data/2.5/forecast?lat=51.7564&lon=-0.3519&units=metric&limit=1&appid=4d9e86afd3e0034d2ad0b63e6c30da28

# to find lattitude, longitude and city name by postcode and country code:   https://api.openweathermap.org/geo/1.0/zip?zip=AL34TL,GB&appid=4d9e86afd3e0034d2ad0b63e6c30da28
# to find lattitude, longitude and country name by city:    http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid=4d9e86afd3e0034d2ad0b63e6c30da28

import pandas as pd
import requests # to use API
import datetime as datetime # to convert into date & time formate
#from datetime import datetime # to show current date & time
import os # to check if csv file already exists before exporting the data into csv. Also to delete CSV file 
import streamlit as st # ipmorts streamlit to create web app using 'app.py' file
import altair as alt # imports altair package
import pytz # to display current date & time
import time # to run python code every 10 minutes using a timer



# Declares variable for default city name
#location = 'St Albans'

def api_request(location): # function to download weather data via API. The function takes 'location' as input and returns 'curr_df' and 'df' DataFrames as output

    # Declares variables for API
    full_api_link_current = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&units=metric&limit=1&appid=4d9e86afd3e0034d2ad0b63e6c30da28"
    full_api_link_forecast = "https://api.openweathermap.org/data/2.5/forecast?q="+location+"&units=metric&limit=1&appid=4d9e86afd3e0034d2ad0b63e6c30da28"
    #filename = 'weather.csv'

    # Create empty lists to populate with values later on
    temp, feels_like, temp_min, temp_max, weather_desc, wind_speed, precipitation, city, date_time, sunrise, sunset, type = ([],[],[],[],[],[],[],[],[],[],[],[])

    def download_API_function(full_api_link): # function to download weather data via API
        api_link = requests.get(full_api_link)
        api_data = api_link.json()
        return api_data

    api_data_current = download_API_function(full_api_link_current) # downloads current weather data via API
    api_data_forecast = download_API_function(full_api_link_forecast) # downloads forecast weather data via API
    #print(api_data_current) # checks if the API request works
    #print(api_data_forecast) # checks if the API request works

    row_num = len(((api_data_forecast['list']))) # finds number of rows in the dataset

    # Parses current weather data
    if api_data_current['cod'] == '404': # if the city doesn't exist, then ask to re-enter correct name
        print("Invalid city: {}, please check you entered it City name correctly".format(location))
    else:
        # extracts current weather data and stores it in relevant list variables
        temp.append(api_data_current['main']['temp'])
        feels_like.append(api_data_current['main']['feels_like'])
        temp_min.append(api_data_current['main']['temp_min'])
        temp_max.append(api_data_current['main']['temp_max'])
        weather_desc.append(api_data_current['weather'][0]['description'])
        wind_speed.append(api_data_current['wind']['speed'])
        try: # using try except method to check if 'rain' value is available and captures it in 'precipitation' list. If 'rain' value is not available, then captures '0'
            precipitation.append(api_data_current['rain']['1h'])
        except KeyError:
            precipitation.append(0)
            pass
        city.append(api_data_current['name'])
        epoch_date = (api_data_current['dt'])
        epoch_sunrise = (api_data_current['sys']['sunrise'])
        epoch_sunset = (api_data_current['sys']['sunset'])
        date_time.append(datetime.datetime.fromtimestamp(epoch_date)) # converts epoch to Datetime
        sunrise.append(datetime.datetime.fromtimestamp(epoch_sunrise)) # converts epoch to Datetime
        sunset.append(datetime.datetime.fromtimestamp(epoch_sunset)) # converts epoch to Datetime
        type.append('Current')
        # extracts current weather data and stores it in relevant list variables
        for x in range(row_num):
            temp.append(api_data_forecast['list'][x]['main']['temp'])
            feels_like.append(api_data_forecast['list'][x]['main']['feels_like'])
            temp_min.append(api_data_forecast['list'][x]['main']['temp_min'])
            temp_max.append(api_data_forecast['list'][x]['main']['temp_max'])
            weather_desc.append(api_data_forecast['list'][x]['weather'][0]['description'])
            wind_speed.append(api_data_forecast['list'][x]['wind']['speed'])
            try: # using try except method to check if 'rain' value is available and captures it in 'precipitation' list. If 'rain' value is not available, then captures '0'
                precipitation.append(api_data_forecast['list'][x]['rain']['3h'])
            except KeyError:
                precipitation.append(0)
                pass
            city.append(api_data_forecast['city']['name'])
            epoch_date_val = (api_data_forecast['list'][x]['dt'])
            epoch_sunrise_val = (api_data_forecast['city']['sunrise'])
            epoch_sunset_val = (api_data_forecast['city']['sunset'])
            date_time.append(datetime.datetime.fromtimestamp(epoch_date_val)) # converts epoch to Datetime
            sunrise.append(datetime.datetime.fromtimestamp(epoch_sunrise_val)) # converts epoch to Datetime
            sunset.append(datetime.datetime.fromtimestamp(epoch_sunset_val)) # converts epoch to Datetime
            type.append('Forecast')

    # Exports historical and forecast weather data to 'df' Pandas DataFrame
    df = pd.DataFrame({'city': city, 'temp': temp, 'feels_like': feels_like, 'temp_min': temp_min, 'temp_max': temp_max, 'wind_speed': wind_speed, 'precipitation': precipitation, 'date_time': date_time, 'sunrise': sunrise, 'sunset': sunset, 'type': type}) # creates empty DataFrame and populates it with data from lists
    df = pd.melt(df, id_vars=['city', 'type', 'date_time', 'sunrise','sunset'], value_vars=['temp', 'feels_like', 'temp_min', 'temp_max', 'wind_speed', 'precipitation']) # gather columns with numbers into rows and show their results under new 'value' column. This is in order to be able to better chart the data.

    # pulls summary weather & timezone data to show in table in streamlit web app at a later stage

    # shows time in different timezones (NYC & London)
    tz_NY = pytz.timezone('America/New_York') 
    datetime_NY = datetime.datetime.now(tz_NY)
    NY_time = "NY time:", datetime_NY.strftime("%H:%M")
    tz_London = pytz.timezone('Europe/London')
    datetime_London = datetime.datetime.now(tz_London)
    LN_time = "London time:", datetime_London.strftime("%H:%M")

    # pulls data that will later be displayed in DataFrame table
    curr_weather = "Weather now", (api_data_current['weather'][0]['description'])
    curr_sunrise = "Sunrise", df.at[0, 'sunrise'].strftime("%H:%M")
    curr_sunset = "Sunset", df.at[0, 'sunset'].strftime("%H:%M")
    curr_date = "Time now", datetime.datetime.now().strftime("%a %d %b %Y %H:%M")
    curr_update_time = "Last updated", df.at[0, 'date_time'].strftime("%H:%M")

    # exports data to DataFrame and formats its for better presentation
    curr_df = pd.DataFrame({curr_date[0]: curr_date[1:], curr_weather[0]: curr_weather[1:], curr_sunrise[0]: curr_sunrise[1:], curr_sunset[0]: curr_sunset[1:], curr_update_time[0]: curr_update_time[1:], LN_time[0]: LN_time[1:], NY_time[0]: NY_time[1:]}) # creates empty DataFrame and populates it with data from lists
    curr_df = curr_df.transpose() # switches rows with columns in DataFrame
    curr_df = curr_df.rename(columns={0: "Values"}) # renames '0' column to 'Values'
    return df, curr_df


# runs 'api_request' function that takes 'location' as input and returns 'curr_df' and 'df' DataFrames as output. These DataFrames will later be used in streamlit web app
api_result = api_request(location='St Albans')
df = api_result[0]
curr_df = api_result[1]


# Streamlit script to turn this python script into wewb app
# instructions here: https://www.youtube.com/watch?v=Sb0A9i6d320

st.set_page_config(page_title='Weather forecast', 
                    page_icon=":bar_chart:", 
                    layout='wide'
) # creates page config file for streamlit web app

st.sidebar.header('Change settings here:') # creates sidebar to select which measures to display, with default selection being 'temp', 'wind_speed', 'precipitation'
select_measures = st.sidebar.multiselect(
    'Select measure to show',
    options=df['variable'].unique(),
    default=['temp', 'precipitation']
)


# function to re-download API data and create a chart and a table based on the city selected through 'select_location' variable below
def create_chart_table(location):

    api_result = api_request(location=location)
    df = api_result[0]
    curr_df = api_result[1]

    df_selection = df.query("variable == @select_measures & city == @location") # to filter table results using fields in the left-hand pane 
    #st.dataframe(df_selection) # show filtered data as DataFrame on streamlit page
    # Creates bar chart
    altchart = alt.Chart(df_selection, title=location).mark_line().encode(
        x=alt.X('date_time:T', axis=alt.Axis(format='%a %H:%M')),
        #x=alt.X('monthdatehours(date_time):T'),
        y='value',
        color='variable'
    ).interactive(bind_y=False) # interactive chart which you can move around and zoom in/out. It shows XY axis line chart, with 'date_time' in X axis in a hours+day+month+year format, 'value' in Y axis for rows where 'value' fields are either 'temp' or 'wind_speed'
    # ).interactive().transform_filter({'field': 'variable', 'oneOf': ['temp', 'wind_speed', 'precipitation']}) # interactive chart which you can move around and zoom in/out. It shows XY axis line chart, with 'date_time' in X axis in a hours+day+month+year format, 'value' in Y axis for rows where 'value' fields are either 'temp' or 'wind_speed'

    # creates two columns and shows chart and table in each of those columns
    left_column, right_column = st.columns([2,1])
    left_column.altair_chart(altchart, use_container_width=True) # shows filtered altair data chart on streamlit page and resizes it to fit the page
    right_column.dataframe(curr_df, use_container_width=True) # shows current time, weather and other data as Pandas DataFrame table on streamlit page and resizes it to fit the page
    # st.altair_chart(altchart, use_container_width=True) # shows filtered altair data on streamlit page and resizes it to fit the page
    # st.dataframe(curr_df, use_container_width=True) # shows current time, weather and other data as Pandas DataFrame table on streamlit page and resizes it to fit the page


select_location = st.sidebar.selectbox("Which city?", ('St Albans', 'London', 'New York', 'Baku', 'Dubai', 'Harare', 'Other (please specify)'), 0) # prompts user to select a city, to show the weather for. By default, 'St Albans' is selected. 

if select_location == 'Other (please specify)':
    location = st.sidebar.text_input(
        'Type another city to show'
    ) # creates sidebar to type a city that's not in the list
    if len(location) > 0:
        select_location = location
        create_chart_table(location=select_location) # launches function to re-download API data and create a chart and a table based on the city selected through 'select_location' variable
else:
    create_chart_table(location=select_location) # launches


st.markdown('---') # to draw solid line on streamlit page
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True) # hides streamlit icons and logo from our web app


#TODO add functionality at the end of the code to wait for X minutes and then refresh API by calling     create_chart_table(select_location)  Try using session states and callbacks explained heer: https://www.youtube.com/watch?v=5l9COMQ3acc&list=PLqJNvqpHr6xOSPYv_xPS32He2sSOE2A7C&index=2
# while(True):
#     create_chart_table(select_location)
#     time.sleep(10)
# OR
# loop = st.sidebar.radio(
#     'Refresh data every 15 minutes?', ('No','Yes')
# )
# if loop == 'Yes':
#     while True:
#         time.sleep(10)
#         api_result = api_request(location="St Albans")
#         df = api_result[0]
#         curr_df = api_result[1]
#         st.write(df.head())
#         st.write(curr_df.head())

#TODO add functionality to show either clock or table (the table is already made) alongside the weather chart

