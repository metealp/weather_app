from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
import requests
from .models import City
from .forms import CityForm
# Create your views here.
@csrf_protect
def index(request):
    err_msg = ''
    message = ''
    message_class = ''
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=bb83f5fe29ffc63a6a7530c425378b6c&lang=tr'
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name'] #taking only name attr from data
            count_cities = City.objects.filter(name=new_city).count() 
            if count_cities == 0: #checking if city already added to db
                resp = requests.get(url.format(new_city)).json()
                if resp['cod'] == 200: #checking for valid city in api
                    form.save()
                else:
                    err_msg = 'City does not exist in the database'
            else:
                err_msg = 'City already exists in page'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'
    form = CityForm() #so user see blank 

    cities = City.objects.all()
    weather_data = []
    for city in cities:
        resp = requests.get(url.format(city)).json()
        city_weather = {
            'city':city.name,
            'temperature': resp['main']['temp'],
            'feels_like': resp['main']['feels_like'],
            'humidity': resp['main']['humidity'],
            'description': resp['weather'][0]['description'],
            'icon': resp['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    return render(request, 'wheater_app/wheater.html', {
        'weather_data':weather_data, 
        'form':form,
        'message': message,
        'message_class': message_class,
        })

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')