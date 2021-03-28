import json
from django.shortcuts import render
from datetime import datetime
from django.contrib import messages
import requests

#weather api
user_api = "Paste your weather api"

#home page
def home(request):
    if request.method == 'POST':
        location = request.POST['loc']
        return render(request, "home.html", {'loc': location})
    return render(request, "home.html")

#Show page after fetch weather
def show(request):
    location = request.GET['loc']
    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + user_api
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()
    #print(api_data)
    if api_data['cod'] == "404":
        messages.warning(
            request,
            f"Invailid city {location.upper()} Please check the city name")
        return render(request, "home.html")
    else:
        city_temp = (api_data['main']['temp']) - 273.15
        wheather_desc = api_data['weather'][0]['description']
        hmdt = api_data['main']['humidity']
        wind_spd = api_data['wind']['speed']
        date_time = datetime.now().strftime("%d %b %y | %I:%M:%S:%p")
        data = {
            'city_temp': city_temp,
            'weahter_desc': wheather_desc,
            'hmdt': hmdt,
            'wind': wind_spd,
            'date_time': date_time,
            'loc': location
        }
        datajson = json.dumps(data)
        return render(request, "home.html", {'data': datajson})
