from tkinter import *
import requests
from datetime import datetime

root = Tk()
root.geometry("500x600")
root.resizable(True, True)
root.title("WeatherWhiz")
root.config(bg='#1f1d19')  # Changed here

def time_format(utc):
    local_time = datetime.utcfromtimestamp(utc)
    return local_time.time()

city_value = StringVar()
recent_searches = []

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

        weather = (f"\nWeather at: {city_name}\nTemperature(°C): {temperature}°"
                   f"\nFeels like(°C): {feels_like}°\nWindspeed: {wind_speed}"
                   f"\nPressure: {pressure} hPa\nHumidity: {humidity}%"
                   f"\nSunrise: {sunrise_time}\nSunset: {sunset_time}"
                   f"\nClouds: {cloudy}%\nInfo: {description}")
        
        if city_name not in recent_searches:
            recent_searches.append(city_name)
            recent_searches_list.insert(END, city_name)

    else:
        weather = f"\n\tWeather for '{city_name}' not found!\n\tPlease enter a valid city!"

    tfield.insert(INSERT, weather)

def refresh():
    city_value.set('')
    tfield.delete('1.0', 'end')

def enable_input(event):
    inp_city.focus_set()

def on_recent_search_select(event):
    selected_index = recent_searches_list.curselection()
    if selected_index:
        selected_city = recent_searches_list.get(selected_index)
        city_value.set(selected_city)
        showWeather()

city_head = Label(root, text='WeatherWhiz Search', font=('Courier', 25, 'bold'), bg='#1f1d19', fg='white')  # Changed here
city_head.pack(pady=5)

inp_city = Entry(root, textvariable=city_value, width=24, font=('Courier', 16, 'bold'), bg='darkgray', fg='black')
inp_city.pack()

Button(root, command=showWeather, text="Check Weather", font=("Courier", 10, 'bold'), bg='green', fg='white',
       activebackground="black", padx=5, pady=5).pack(pady=20)

refresh_button = Button(root, command=refresh, text="Refresh", font=("Courier", 10, 'bold'), bg='olive', fg='white',
                        activebackground="black", padx=5, pady=5)
refresh_button.pack(pady=10)

weather_now = Label(root, text="Weather at your city:", font=('Courier', 12, 'bold'), bg='#1f1d19', fg='white')  # Changed here
weather_now.pack(pady=10)

tfield = Text(root, width=46, height=10, bg='darkgray', font=('Courier', 12))
tfield.pack()

recent_searches_label = Label(root, text="Recent Searches:", font=('Courier', 12, 'bold'), bg='#1f1d19', fg='white')  # Changed here
recent_searches_label.pack(pady=5)

recent_searches_list = Listbox(root, width=46, height=5, bg='darkgray', font=('Courier', 12))
recent_searches_list.pack()

# Bind the selection event to the on_recent_search_select function
recent_searches_list.bind('<<ListboxSelect>>', on_recent_search_select)

root.bind("<FocusIn>", enable_input)

root.mainloop()
