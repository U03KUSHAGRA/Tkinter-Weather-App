from tkinter import*
import requests
import json
from datetime import datetime

root =Tk()
root.geometry("500x500")
root.resizable(0,0) 
root.title("Weather")

def time_format(utc):
    local_time = datetime.utcfromtimestamp(utc)
    return local_time.time()

city_value = StringVar()

def showWeather():
    api_key = "263cf15f949187041d08ab0679f24032"
    city_name = city_value.get()
    weather_url = (f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}')
    response = requests.get(weather_url) 
    weather_info = response.json()
    tfield.delete('1.0', 'end')  

    if weather_info['cod'] == 200:
        kelvin = 273 
        temperature = int(weather_info['main']['temp'] - kelvin)                                    
        feels_like = int(weather_info['main']['feels_like'] - kelvin)
        sunrise = weather_info['sys']['sunrise']
        sunset = weather_info['sys']['sunset']
        pressure = weather_info['main']['pressure']
        humidity = weather_info['main']['humidity']
        wind_speed = weather_info['wind']['speed'] * 3.6
        timezone = weather_info['timezone']
        cloudy = weather_info['clouds']['all']
        description = weather_info['weather'][0]['description']
        sunrise_time = time_format(sunrise + timezone)
        sunset_time = time_format(sunset + timezone)
        
        weather = f"\nWeather at: {city_name}\nTemperature(°C): {temperature}°\nFeels like(°C): {feels_like}°\nWindspeed: {wind_speed}\nPressure: {pressure} hPa\nHumidity: {humidity}%\nSunrise: {sunrise_time}\nSunset: {sunset_time}\nClouds: {cloudy}%\nInfo: {description}"
    else:
        weather = f"\n\tWeather for '{city_name}' not found!\n\Please enter a valid city!"

    tfield.insert(INSERT, weather)  

city_head= Label(root, text = 'Enter City Name', font = 'Courier 25 bold').pack(pady=10)
inp_city = Entry(root, textvariable = city_value,  width = 24, font='Courier 16 bold').pack()
Button(root, command = showWeather, text = "Check Weather", font="Courier 10 bold", bg='green', fg='black', activebackground="black", padx=5, pady=5 ).pack(pady= 20)
weather_now = Label(root, text = "Weather at your city:", font = 'Courier 12 bold').pack(pady=10)
tfield = Text(root, width=46, height=10)
tfield.pack()
root.mainloop()