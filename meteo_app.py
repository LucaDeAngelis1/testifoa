import joblib
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io
import requests
import os

from dotenv import load_dotenv

#load_dotenv('.env')
load_dotenv()
#API_key : str = os.getenv('api_key')
API_key = os.getenv('api_key')


def prevmeteo(city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}'
    result = requests.get(url)
    if result:
        json = result.json()
        temp_min = json['main']['temp_min']-273.15
        temp = json['main']['temp']-273.15
        temp_max = json['main']['temp_max']-273.15
        pressure = json['main']['pressure']
        humidity = json['main']['humidity']
        wind_speed = json['wind']['speed']
        country = json['sys']['country']
        name = json['name']
        res = [name, country, round(temp_min,1), round(temp,1), round(temp_max,1), pressure, humidity, round(wind_speed,2)]
        return res, json
    else:
        print("Città non trovata")



def main():
    st.title("Meteo")

    col1, col2 = st.columns(2)

    with col1:
        city_name = st.text_input("Select a city")
    
    with col2:
        if city_name:
            res, json = prevmeteo(city_name)
            st.info('Name: ' + str(res[7]))
            st.info('Country: ' + str(res[6]))
            st.info('T min °C: ' + str(round(res[0],2)))
            st.success('T °C: ' + str(round(res[1],2)))
            st.info('T max °C: ' + str(round(res[2],2)))
            st.info('Pressure: ' + str(res[3],2))
            st.info('Humidity %: ' + str(round(res[4],2)))
            st.info('Wind speed m/s: ' + str(res[5],2))
            
            
            #st.subheader('Dettagli')



if __name__ == "__main__":
    main()